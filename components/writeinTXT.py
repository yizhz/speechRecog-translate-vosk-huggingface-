import suanpan
from suanpan.app import app
from suanpan.log import logger
from suanpan.app.arguments import String, Int

@app.param(String(key="param1", alias="save_file"))
@app.afterInit
def createFile(context):
    args=context.args
    save_file=args["save_file"]
    f= open(save_file, "w", encoding='utf-8')
    f.close()

@app.input(String(key="inputData1", default="Suanpan"))
@app.output(String(key="out1", alias="msgout1"))
def saveTXT(context):
    args=context.args
    text=args.inputData1
    save_file=args.save_file
    if save_file is not None:
        f= open(save_file, "a", encoding='utf-8')
        f.write(text+"\n"+"\n")
        f.flush()    