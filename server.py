from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

import acct

DATAFILE = 'site/data/ledger.csv'
ACCTFILE = 'site/data/account.csv'

origins = [
    '*',
    ]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    )

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    data = dict(request=request, appname='hello')
    return templates.TemplateResponse('index.html', data)


@app.get('/app-2', response_class=HTMLResponse)
async def app_2(request: Request):
    data = dict(request=request, appname='app-2', title='app-2')
    return templates.TemplateResponse('app-2.html', data)


@app.get('/app-3', response_class=HTMLResponse)
async def app_3(request: Request):
    data = dict(request=request, appname='app-3', title='app-3')
    return templates.TemplateResponse('app-3.html', data)


@app.get('/app-4', response_class=HTMLResponse)
async def app_4(request: Request):
    data = dict(request=request, appname='app-4', title='app-4')
    return templates.TemplateResponse('app-4.html', data)


@app.get('/app-5', response_class=HTMLResponse)
async def app_5(request: Request):
    data = dict(request=request, appname='app-5', title='app-5')
    return templates.TemplateResponse('app-5.html', data)


@app.get('/app-6', response_class=HTMLResponse)
async def app_6(request: Request):
    data = dict(request=request, appname='app-6', title='app-6')
    return templates.TemplateResponse('app-6.html', data)


@app.get('/comp-1', response_class=HTMLResponse)
async def comp_1(request: Request):
    data = dict(request=request, appname='comp-1', title='comp-1')
    return templates.TemplateResponse('comp-1.html', data)


@app.get('/list1', response_class=HTMLResponse)
async def list1(request: Request):
    data = dict(request=request)
    return templates.TemplateResponse('list1.html', data)


@app.get('/select1', response_class=HTMLResponse)
async def select1(request: Request):
    data = dict(request=request, url='/data/month')
    return templates.TemplateResponse('select1.html', data)


@app.get('/bootstrap1', response_class=HTMLResponse)
async def bootstrap1(request: Request):
    data = dict(request=request,
                title='bootstrap',
                appname='bootstrap',
                message='こんにちは世界')
    return templates.TemplateResponse('bootstrap1.html', data)


@app.get('/bootstrap2', response_class=HTMLResponse)
async def bootstrap2(request: Request):
    data = dict(request=request,
                title='bootstrap',
                appname='bootstrap')
    return templates.TemplateResponse('bootstrap2.html', data)


@app.get('/data/grocery')
async def data_grocery(response: Response):
    import pandas as pd
    names = 'id value'.split()
    df = pd.read_csv('data/grocery.csv', header=None, names=names)
    response.headers['Cache-Control'] = 'no-cache, no-store'
    return df.to_dict(orient='records')


@app.get('/data/month')
async def data_month(response: Response):
    import pandas as pd
    names = 'id value name'.split()
    df = pd.read_csv('data/month.csv', header=None, names=names)
    response.headers['Cache-Control'] = 'no-cache, no-store'
    return df.to_dict(orient='records')


def read_csv(datafile=DATAFILE):
    return acct.read_csv(datafile)


def read_acct_csv(datafile=ACCTFILE):
    return acct.read_accounts_csv(datafile)


@app.get('/api/v1/ledger')
async def api_ledger(response: Response):
    df = read_csv()
    account = '資産:現金:家計財布'
    data = df.loc[df['account']==account]
    data['cum'] = data['amount'].cumsum()
    return data.to_dict(orient='records')


@app.get('/api/v1/accounts')
async def api_accounts(response: Response):
    df = read_acct_csv()
    return df.to_dict(orient='records')
