import suanpan
from suanpan.app import app
from suanpan.log import logger
from suanpan.app.arguments import String, Int
from suanpan import g

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

@app.param(String(key="param1", alias="from_lang"))
@app.param(String(key="param2", alias="to_lang"))
@app.afterInit
def loadModel(context):
    args=context.args
    from_lang=args['param1']
    to_lang=args['param2']
    logger.info('Start downloading the model!')
    g.tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-"+from_lang+"-"+to_lang)
    g.model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-"+from_lang+"-"+to_lang)
    logger.info('Finish downloading the model!')

@app.input(String(key="inputData1", default="Suanpan"))
@app.output(String(key="out1", alias="msgout1"))
def translate(context):
    args=context.args
    text=args.inputData1
    batch = g.tokenizer.prepare_seq2seq_batch(src_texts=[text], return_tensors='pt', max_length=512)
    translation = g.model.generate(**batch)
    result = g.tokenizer.batch_decode(translation, skip_special_tokens=True)
    return result


if __name__ == '__main__':
    suanpan.run(app)
