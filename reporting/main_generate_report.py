import datapane as dp
import os

filenameReport = r"my_app.html"



## NO TOUCHI ------- 
reportingDirectory = "reporting"




def main():
    blocks =    [   dp.Text("Hello, world!"),
                    dp.Text("This is my first Datapane report!")
                ]
    
    my_page = dp.Page(blocks=blocks)

    app = dp.App(blocks=my_page.blocks)

    ## SAVE TO HTML FILE
    app.save(path=os.path.join(reportingDirectory, filenameReport),
        formatting=dp.AppFormatting(
            light_prose=False,
            accent_color="#90288D",
            bg_color="#FFFFFF",
            text_alignment=dp.TextAlignment.LEFT,
            font=dp.FontChoice.DEFAULT,
            width=dp.AppWidth.MEDIUM,
        ),
    )

    ## SAVE TO PDF FILE

    ## DEPLOY TO NGROK
    dp.serve_app(app, public=True)
    # dp.serve_app(app, public=False, embed_mode=True)


if __name__=='__main__':
    main()
    #exit()