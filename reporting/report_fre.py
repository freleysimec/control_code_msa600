import sys
import numpy as np
import pandas as pd
import datapane as dp
import datetime
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
pio.templates.default = "plotly_dark"
import statistics as st

rawDataFile = r'C:\Users\samsom43\OneDrive - imec\Documents\230220 automated wafer mapping results.csv'
dieMappingFile = r'C:\Users\samsom43\OneDrive - imec\Documents\DieMapping.csv'

# initialize datapane app dictionnary
dp_dict = {}
report_title = 'CANOPUS MMA Brownian frequency measurement report'
report_date = datetime.datetime.now()
report_version = '00-01'
report_reference = 'CAN-TR-0001-' + report_version + '-' + report_date.strftime('%y%m%d%H%M%S')
section_number = 0
subsection_number = 0

def add_page(page_title):
    global section_number
    global subsection_number
    dp_dict[page_title] = []
    page_number = len(dp_dict)
    dp_dict[page_title].append('# ' + report_title)
    dp_dict[page_title].append(f'<small>page {page_number} - confidential</small>')
    dp_dict[page_title].append('## ' + str(page_number) + ' ' + page_title)
    section_number = 0
    subsection_number = 0

def add_section(section_title):
    global section_number
    global subsection_number
    page_number = len(dp_dict)
    section_number = section_number + 1
    dp_dict[list(dp_dict)[-1]].append('### ' + str(page_number) + '.' + str(section_number) + ' ' + section_title)
    subsection_number = 0

def add_subsection(section_title):
    global section_number
    global subsection_number
    page_number = len(dp_dict)
    subsection_number = subsection_number + 1
    dp_dict[list(dp_dict)[-1]].append('#### ' + str(page_number) + '.' + str(section_number) + '.' + str(subsection_number) + ' ' + section_title)

def add_block(block):
    dp_dict[list(dp_dict)[-1]].append(block)
        
#add_page('Intro')
add_page('Intro')
add_section('Intro')
add_block('This is an automatically generated report presenting Canopus MMA Brownian resonance frequency test.')
add_block(dp.Text(f"""<i>Report reference : </i>{report_reference}                               
<i>Generation date : </i>{report_date.strftime('%d/%m/%Y')}                               
<i>Generator version : </i>{report_version}"""))

raw_data = pd.read_csv(rawDataFile)
#raw_data2 = pd.read_csv(r'C:\Users\samsom43\OneDrive - imec\Documents\230220 automated wafer mapping results.csv')
##raw_data2['wafer number']=99
#raw_data=pd.concat([raw_data,raw_data2])
die_mapping = pd.read_csv(dieMappingFile)

w=raw_data['wafer number'].unique()
#ww=np.array2string(w)
ww=np.array_str(w)
Wafer = 'Wafer: ' + ww[:]
#Wafer=Wafer.format(ww[:])
add_block(dp.Text('Devices under test, FL1, ' + Wafer  ))
#print(raw_data['wafer number'].unique())

add_block(dp.Text("""Each die has two measurements or positions.
The average of the 2 measurements are used to calculate the mean per mirror.
The difference between the 2 positions is used to calculate the measurement error"""))


diex=[]
diey=[]
for r in raw_data['die index']:
    #print(r)
    die = die_mapping.iloc[r,:]    
    diex.append(int(die['DieX']+4))
    diey.append(int(die['DieY']+4))
   
#raw_data3 = raw_data
raw_data['DieX']=diex
raw_data['DieY']=diey
   
filtered=0
while filtered<2:
    devs = 0
    while devs<2:
        test_results = raw_data.copy()
        test_results=test_results.dropna()
    
        if filtered==2:
            x=np.where(test_results['Good mirrors']=='all')
            test_results=test_results.iloc[x]

        #add_section('Summary')
    
        if devs==0:
            #add_section('dev1')
            device='Dev3'
            x=np.where(test_results['structure index']==0)
            Fmax = 4500
            Fmin = 3200
            Pmax = 11000
            Pmin = 8500
        else:
            #add_section('dev3')
            device='Dev1'
            x=np.where(test_results['structure index']==1)
            Fmax = 3400
            Fmin = 2000
            Pmax = 9600
            Pmin = 7500
        MaxTiltError=2


        if filtered == 0:
            filt='Raw'
        if filtered == 1:
            filt='Filtered'

        
            
        test_results=test_results.iloc[x]    
        
        mx=test_results.iloc[:,0:11]  #test_results.iloc[:,11:15]
        mx['DieX']= test_results.iloc[:]['DieX']   
        mx['DieY']= test_results.iloc[:]['DieY']
        mx['Die']= test_results.iloc[:]['DieX']+10*test_results.iloc[:]['DieY']
        mx['Wafer']= test_results.iloc[:]['wafer number']
        #mx=mx.dropna()
        
        mc=mx.copy()
        mc['mirror']='mc'
        mc['Piston']=(test_results['RF Piston 1']+test_results['RF Piston 2'])/2
        mc['Tilt']=(test_results['RF Tilt 1']+test_results['RF Tilt 2'])/2
        mc['PistonError']=(100*(test_results['RF Piston 1']-test_results['RF Piston 2'])/mc['Piston']/2)
        mc['TiltError']=(100*(test_results['RF Tilt 1']-test_results['RF Tilt 2'])//mc['Tilt']/2)
        x=np.where(test_results['die index']==27)
        if filtered==1:   mc=mc.iloc[np.where(abs(mc['TiltError'])<MaxTiltError)]
        if filtered==1:   mc=mc.iloc[np.where(mc['Tilt']<Fmax)]
        if filtered==1:   mc=mc.iloc[np.where(mc['Tilt']>Fmin)]
        if filtered==1:   mc=mc.iloc[np.where(mc['Piston']<Pmax)]
        if filtered==1:   mc=mc.iloc[np.where(mc['Piston']>Pmin)]
        
        ml=mx.copy()
        ml['mirror']='ml'
        ml['Piston']=(test_results['RF Piston 3']+test_results['RF Piston 4'])/2
        ml['Tilt']=(test_results['RF Tilt 3']+test_results['RF Tilt 4'])/2
        ml['PistonError']=(100*(test_results['RF Piston 3']-test_results['RF Piston 4'])/ml['Piston']/2)
        ml['TiltError']=(100*(test_results['RF Tilt 3']-test_results['RF Tilt 4'])//ml['Tilt']/2)
        if filtered==1:   ml=ml.iloc[np.where(abs(ml['TiltError'])<MaxTiltError)]
        if filtered==1:   ml=ml.iloc[np.where(ml['Tilt']<Fmax)]
        if filtered==1:   ml=ml.iloc[np.where(ml['Tilt']>Fmin)]
        if filtered==1:   ml=ml.iloc[np.where(ml['Piston']<Pmax)]
        if filtered==1:   ml=ml.iloc[np.where(ml['Piston']>Pmin)]
       
        mt=mx.copy()
        mt['mirror']='mt'
        mt['Piston']=(test_results['RF Piston 5']+test_results['RF Piston 6'])/2
        mt['Tilt']=(test_results['RF Tilt 5']+test_results['RF Tilt 6'])/2
        mt['PistonError']=(100*(test_results['RF Piston 5']-test_results['RF Piston 6'])/mt['Piston']/2)
        mt['TiltError']=(100*(test_results['RF Tilt 5']-test_results['RF Tilt 6'])//mt['Tilt']/2)
        if filtered==1:   mt=mt.iloc[np.where(abs(mt['TiltError'])<2)]
        if filtered==1:   mt=mt.iloc[np.where(mt['Tilt']<Fmax)]
        if filtered==1:   mt=mt.iloc[np.where(mt['Tilt']>Fmin)]
        if filtered==1:   mt=mt.iloc[np.where(mt['Piston']<Pmax)]
        if filtered==1:   mt=mt.iloc[np.where(mt['Piston']>Pmin)]
        
        mr=mx.copy()
        mr['mirror']='mr'
        mr['Piston']=(test_results['RF Piston 7']+test_results['RF Piston 8'])/2
        mr['Tilt']=(test_results['RF Tilt 7']+test_results['RF Tilt 8'])/2
        mr['PistonError']=(100*(test_results['RF Piston 7']-test_results['RF Piston 8'])/mr['Piston']/2)
        mr['TiltError']=(100*(test_results['RF Tilt 7']-test_results['RF Tilt 8'])//mr['Tilt']/2)
        if filtered==1:   mr=mr.iloc[np.where(abs(mr['TiltError'])<2)]
        if filtered==1:   mr=mr.iloc[np.where(mr['Tilt']<Fmax)]
        if filtered==1:   mr=mr.iloc[np.where(mr['Tilt']>Fmin)]
        if filtered==1:   mr=mr.iloc[np.where(mr['Piston']<Pmax)]
        if filtered==1:   mr=mr.iloc[np.where(mr['Piston']>Pmin)]
        
        mb=mx.copy()
        mb['mirror']='mb'
        mb['Piston']=(test_results['RF Piston 9']+test_results['RF Piston 10'])/2
        mb['Tilt']=(test_results['RF Tilt 9']+test_results['RF Tilt 10'])/2
        mb['PistonError']=(100*(test_results['RF Piston 9']-test_results['RF Piston 10'])/mb['Piston']/2)
        mb['TiltError']=(100*(test_results['RF Tilt 9']-test_results['RF Tilt 10'])//mb['Tilt']/2)
        if filtered==1:   mb=mb.iloc[np.where(abs(mb['TiltError'])<2)]
        if filtered==1:   mb=mb.iloc[np.where(mb['Tilt']<Fmax)]
        if filtered==1:   mb=mb.iloc[np.where(mb['Tilt']>Fmin)]
        if filtered==1:   mb=mb.iloc[np.where(mb['Piston']<Pmax)]
        if filtered==1:   mb=mb.iloc[np.where(mb['Piston']>Pmin)]
        
        test_results2=pd.concat([mc,ml,mt,mr,mb])
        mc2=mc.copy()
        ml2=ml.copy()
        mt2=mt.copy()
        mr2=mr.copy()
        mb2=mb.copy()
        
        if len(w)>1:
            w=np.concatenate(([0],w))   #add wfr 0 to collect results all wafers
        for wfr in w:
            if wfr!=0:   #'all':
                mc=mc2.iloc[np.where(mc2['Wafer']==wfr)]
                ml=ml2.iloc[np.where(ml2['Wafer']==wfr)]
                mt=mt2.iloc[np.where(mt2['Wafer']==wfr)]
                mr=mr2.iloc[np.where(mr2['Wafer']==wfr)]
                mb=mb2.iloc[np.where(mb2['Wafer']==wfr)]
            test_results2=pd.concat([mc,ml,mt,mr,mb])
            
            if (wfr==0): 
                wfr='all'
                add_page(filt + ' Data ' + device)
            if (len(w)==1):
                add_page(filt + ' Data ' + device)
            add_section(filt + ' Data ' + device + ': Wafer ' + str(wfr))                    

            if filtered == 0:
                add_block(dp.Text('This section is taking the raw data as is, in the next section outliers are filtered from the dataset'))
            if filtered == 1:
                f = 'Filtering1: ' + str(Fmin) + 'Hz < F_Tilt < ' + str(Fmax) + 'Hz, and ' + str(Pmin) + 'Hz < F_Piston < ' + str(Pmax) + 'Hz'
                add_block(dp.Text(f))
                f = 'Filtering2: Error between Tilt frequency measurement of 2 positions < ' + str(MaxTiltError) + '%'
                add_block(dp.Text(f))
                       
            if (filtered>0) and (wfr != 'all'):
                samples = mc['Die']
                good_sample=[]        
                for s in samples:
                    ss=np.where(test_results2['Die']==s)
                    if len(ss[0][:])==5:  
                        good_sample.append(s)
                add_block('Nr of devices with all good mirrors: ' + str(len(good_sample)))
                add_block('Good samples: ' + str(np.sort(good_sample)))                     
            
            error2 = {'mirror':['mc','ml','mt','mr','mb']}
            error2 = pd.DataFrame(error2)
            #error2['Wafer']=[np.average(mc['Wafer']),np.average(ml['Wafer']),np.average(mt['Wafer']),np.average(mr['Wafer']),np.average(mb['Wafer'])]
            #error2['Wafer']=[wfr,wfr,wfr,wfr,wfr]
            error2['TiltMean[Hz]']=[np.average(mc['Tilt']),np.average(ml['Tilt']),np.average(mt['Tilt']),np.average(mr['Tilt']),np.average(mb['Tilt'])]
            error2['TiltStdev[Hz]']=[st.stdev(mc['Tilt']),st.stdev(ml['Tilt']),st.stdev(mt['Tilt']),st.stdev(mr['Tilt']),st.stdev(mb['Tilt'])]
            error2['TiltErrMean[%]']=[np.average(mc['TiltError']),np.average(ml['TiltError']),np.average(mt['TiltError']),np.average(mr['TiltError']),np.average(mb['TiltError'])]
            error2['TiltErrStdev[%]']=[st.stdev(mc['TiltError']),st.stdev(ml['TiltError']),st.stdev(mt['TiltError']),st.stdev(mr['TiltError']),st.stdev(mb['TiltError'])]
            error2['NrMeas']=[len(mc),len(ml),len(mt),len(mr),len(mb)]
            
            add_subsection('Summary Tilt')
            add_block(dp.DataTable(error2))
            
            fig = px.histogram(test_results2, x='Tilt',labels={'Tilt':'Tilt [Hz]'})
            add_block(dp.Plot(fig, caption='Tilt all mirrors [Hz]'))
    
            fig=go.Figure()
            fig.add_trace(go.Histogram(x=mc['Tilt'],name='mc'))
            fig.add_trace(go.Histogram(x=ml['Tilt'],name='ml'))
            fig.add_trace(go.Histogram(x=mt['Tilt'],name='mt'))
            fig.add_trace(go.Histogram(x=mr['Tilt'],name='mr'))
            fig.add_trace(go.Histogram(x=mb['Tilt'],name='mb'))
            #fig.update_layout(barmode='stack')
            add_block(dp.Plot(fig, caption='Tilt [Hz]'))  
                          
            error = {'mirror':['mc','ml','mt','mr','mb']}
            error = pd.DataFrame(error)
            #error['Wafer']=[np.average(mc['Wafer']),np.average(ml['Wafer']),np.average(mt['Wafer']),np.average(mr['Wafer']),np.average(mb['Wafer'])]
            error['PistonMean[Hz]']=[np.average(mc['Piston']),np.average(ml['Piston']),np.average(mt['Piston']),np.average(mr['Piston']),np.average(mb['Piston'])]
            error['PistonStdev[Hz]']=[st.stdev(mc['Piston']),st.stdev(ml['Piston']),st.stdev(mt['Piston']),st.stdev(mr['Piston']),st.stdev(mb['Piston'])]
            error['PistonErrMean[%]']=[np.average(mc['PistonError']),np.average(ml['PistonError']),np.average(mt['PistonError']),np.average(mr['PistonError']),np.average(mb['PistonError'])]
            error['PistonErrStdev[%]']=[st.stdev(mc['PistonError']),st.stdev(ml['PistonError']),st.stdev(mt['PistonError']),st.stdev(mr['PistonError']),st.stdev(mb['PistonError'])]
            error['NrMeas']=[len(mc),len(ml),len(mt),len(mr),len(mb)]
            
            add_subsection('Summary Piston')
            add_block(dp.DataTable(error))
            
            fig = px.histogram(test_results2, x='Piston', labels={'Piston':'Piston [Hz]'})
            add_block(dp.Plot(fig, caption='Piston all mirrors [Hz]'))
        
        
            add_subsection('Tilt')
            #fig = px.scatter(test_results2, x='die index', y='Tilt', color='mirror', labels={'die index': 'Die Nr', 'Tilt':'Tilt [Hz]'})
            fig = px.scatter(test_results2, x='Die', y='Tilt', color='mirror', labels={'Die': 'DieX+10*DieY', 'Tilt':'Tilt [Hz]'})
            add_block(dp.Plot(fig, caption='Tilt'))
    
                   
            fig1 = dp.Plot(px.scatter(mc, x='DieX', y='DieY', size='Tilt', color='Tilt'), caption='MC Tilt')
            fig2 = dp.Plot(px.scatter(ml, x='DieX', y='DieY', size='Tilt', color='Tilt'), caption='ML Tilt')
            fig3 = dp.Plot(px.scatter(mt, x='DieX', y='DieY', size='Tilt', color='Tilt'), caption='MT Tilt')
            fig4 = dp.Plot(px.scatter(mr, x='DieX', y='DieY', size='Tilt', color='Tilt'), caption='MR Tilt')
            fig5 = dp.Plot(px.scatter(mb, x='DieX', y='DieY', size='Tilt', color='Tilt'), caption='MB Tilt')
            add_block(dp.Group(fig1, fig2, fig3, fig4, fig5, columns = 3))
        
    
            add_subsection('Piston')
           
            fig = px.scatter(test_results2, x='experiment index', y='Piston', color='mirror')
            #fig = px.scatter(test_results2, x='die index', y='Piston', color='mirror', labels={'die index': 'Die Nr', 'Piston':'Piston [Hz]'})
            fig = px.scatter(test_results2, x='Die', y='Piston', color='mirror', labels={'Die': 'DieX+10*DieY', 'Piston':'Piston [Hz]'})
            add_block(dp.Plot(fig, caption='Piston'))
            
                   
            fig1 = dp.Plot(px.scatter(mc, x='DieX', y='DieY', size='Piston', color='Piston'), caption='MC Piston')
            fig2 = dp.Plot(px.scatter(ml, x='DieX', y='DieY', size='Piston', color='Piston'), caption='ML Piston')
            fig3 = dp.Plot(px.scatter(mt, x='DieX', y='DieY', size='Piston', color='Piston'), caption='MT Piston')
            fig4 = dp.Plot(px.scatter(mr, x='DieX', y='DieY', size='Piston', color='Piston'), caption='MR Piston')
            fig5 = dp.Plot(px.scatter(mb, x='DieX', y='DieY', size='Piston', color='Piston'), caption='MB Piston')
            add_block(dp.Group(fig1, fig2, fig3, fig4, fig5, columns = 3))
            #add_block(dp.Group(dp.Plot(fig, caption='MC Piston'), dp.Plot(fig, caption='MC Piston'), columns = 2))

        
        devs += 1
        blaat=1
    filtered += 1
       
 
    
# generate datapane app
dp_list = []
for page_number, page in enumerate(dp_dict):
    dp_list.append(dp.Page(blocks=dp_dict[page], title=str(page_number+1) + ' ' + page))
#app = dp.App(blocks=dp_list,layout=dp.PageLayout.SIDE)
app = dp.App(blocks=dp_list)
app.save(path=r"BrownianMeasReport.html",
        formatting=dp.AppFormatting(
            light_prose=False,
            accent_color="#90288D",
            bg_color="#FFFFFF",
            text_alignment=dp.TextAlignment.LEFT,
            font=dp.FontChoice.DEFAULT,
            width=dp.AppWidth.MEDIUM,
        ),
    )

