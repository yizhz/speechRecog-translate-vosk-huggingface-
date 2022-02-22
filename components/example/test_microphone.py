#!/usr/bin/env python3
import suanpan
from suanpan.app import app
from suanpan.log import logger
from suanpan.app.arguments import String, Int
from suanpan import g

import os
import queue
import sounddevice as sd
import vosk
import sys
#from openpyxl import Workbook
# import xlwt,xlrd
# from xlutils.copy import copy

@app.input(String(key="inputData1", default="Suanpan"))
#@app.param(Bool(key="param1", alias="list_devices",default=False))
@app.param(String(key="param1", alias="list_devices"))
@app.param(Int(key="param2", alias="device"))
@app.param(String(key="param3", alias="model"))
@app.param(Int(key="param4", alias="samplerate"))
@app.param(String(key="param5", alias="save_file"))
@app.output(String(key="out1", alias="msgout1"))
@app.output(String(key="out2", alias="msgout2"))
def microphone(context):
    args = context.args
    logger.info(args)
    save_file=args.save_file
    if save_file is not None:
        f= open(save_file, "w", encoding='utf-8')    
    # g.data = xlrd.open_workbook(args.save_file,formatting_info=True)
    # g.excel = copy(wb=g.data) # 完成xlrd对象向xlwt对象转换
    # g.excel_table = g.excel.get_sheet(0) # 获得要操作的页
    # g.table = g.data.sheets()[0]
    # nrows = g.table.nrows # 获得行数

    #openpyxl
    # workbook = Workbook()
    # g.save_file = args.save_file
    # g.worksheet = workbook.active
    # g.worksheet.title = "Sheet1"
    q = queue.Queue()
    def callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        q.put(bytes(indata))

    if eval(args.list_devices):
        return sd.query_devices(), None

    if args.model is None:
        logger.info("Please add the model path")

    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    model = vosk.Model(args.model)


    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
                            channels=1, callback=callback):
            logger.info('#' * 80)
            rec = vosk.KaldiRecognizer(model, args.samplerate) #注释掉测试卡住运行的代码
            results = []
            finalresults = []        
            while True:
                data = q.get() #注释掉测试卡住运行的代码，是他卡的

                if rec.AcceptWaveform(data):    #注释掉测试卡住运行的代码
                    finalresults.append(rec.Result())
                    showfinalsub=finalresults[-1:]
                    finalsubtitle= ','.join(str(i) for i in showfinalsub)
                    finalsubtitle=finalsubtitle.replace('{','').replace('  "text" : ','').replace('},','').replace('}','').replace('"','')
                    # openpyxl
                    # g.worksheet.append(showfinalsub)

                    # txt
                    if save_file is not None:
                        f.write(finalsubtitle)
                        f.flush()
                    app.send((None,finalsubtitle),context)                    

                else:
                    results.append(rec.PartialResult())
                    showsub=results[-1:] #showsub is a list
                    subtitle= ','.join(str(i) for i in showsub) #list2string for the last element
                    subtitle=subtitle.replace('{','').replace('  "partial" : ','').replace('},','').replace('}','').replace('"','')
                    app.send((subtitle,None), context) 




# @app.beforeExit
# def savefile(context):
#     g.workbook.save(filename=g.save_file)
#     logger.info("Safe successfully!")
    

if __name__ == '__main__':
    suanpan.run(app)