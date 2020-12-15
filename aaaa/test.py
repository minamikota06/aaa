import gspread
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
from apiclient.errors import HttpError

# API情報
DEVELOPER_KEY = 'AIzaSyCqdobpOlkrm1wIGRlHcL4tkRoDpJRSsxA'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(
    YOUTUBE_API_SERVICE_NAME, 
    YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY
    )

search_response = youtube.search().list(
  q='ヒカキン',
  part='id,snippet',
).execute()

#その他のパラメーターはAPIから情報を取得するパラメータと同じ
def get_video_info(part, q, order, type, num):
    dic_list = []
    search_response = youtube.search().list(part=part,q=q,order=order,type=type)
    output = youtube.search().list(part=part,q=q,order=order,type=type).execute()

    #一度に5件しか取得できないため何度も繰り返して実行
    for i in range(num):        
        dic_list = dic_list + output['items']
        search_response = youtube.search().list_next(search_response, output)
        output = search_response.execute()

    df = pd.DataFrame(dic_list)
    #各動画毎に一意のvideoIdを取得
    df1 = pd.DataFrame(list(df['id']))['videoId']
    #各動画毎に一意のvideoIdを取得必要な動画情報だけ取得
    df2 = pd.DataFrame(list(df['snippet']))[['channelTitle','publishedAt','channelId','title','description']]
    ddf = pd.concat([df1,df2], axis = 1)

    return ddf

print(search_response)
get_video_info(part='snippet',q='ボードゲーム',order='viewCount',type='video',num = 20)

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('tube-d2aad8169b7f.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open('apitest').sheet1

# wks.update_acell('A1', 'Hello World!')
# for key in search_response:
#     print(key['title']) # titleのみ参照
# print(wks.acell('A1'))