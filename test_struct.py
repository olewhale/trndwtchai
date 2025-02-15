def process_clients():
    clients = get_all_client()  # выбрать из базы, Notion, Google Sheets и т.д.
    
    for client in clients:
        process_client(client)


def process_client(client):
    accounts = get_all_accounts(client)  # выбрать из базы, Notion, Google Sheets и т.д.
    
    for account in accounts:
        process_account(account)
        

def process_account(account):
    reels = get_all_reels(account)  # выбрать из базы, Notion, Google Sheets и т.д.
    
    for reel in reels:
        reel_json = process_reel(reel)


async def process_reel(reel):
    # обработка реела
    save_to_google(reel_json)


Table: clients
    * id
    * name
    * email

Table: client_accounts
    * id
    * client_id
    * account_id

Table: video_group
    * id
    * type: account / hashtag / location
    * url
    
Table: video_group_video
    * id
    * video_group_id
    * video_id
    
Table: video
    * id
    * account_url
    * url
    * likes
    * comments
    * views
    * date
    * hashtags
    * location
    * music_info
    * duration
