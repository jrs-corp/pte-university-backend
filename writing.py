import os

def sample_extract_key_phrases():
    
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient

    endpoint = os.environ["AZURE_TEXT_ANALYTICS_ENDPOINT"]
    key = os.environ["AZURE_TEXT_ANALYTICS_KEY"]

    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    result = text_analytics_client.extract_key_phrases([ "Montreal is North America’s number one host city for international events. Montreal is home to the famous Cirque de Soleil and hosted the Summer Olympics in 1976. Montreal also played host to Expo 67, considered to be the most successful world’s fair in the 20th Century. Montreal has a very vibrant scene with the Montreal International Jazz Festival, the Just For Laughs Festival, the International Fireworks Festival, Les FrancoFolies de Montréal, the Montreal Beer Festival, the Montreal Reggae Festival, the International Film Festival on Art, International Festival of Circus Arts, Divers/Cité Gay and Lesbian Pride, Blue Metropolis International Literary Festival, the Montreal Grand Prix and many, many more." ])
    answer1 = ['Blue Metropolis International Literary Festival', 'famous Cirque de Soleil', 'number one host city', 'Montreal International Jazz Festival', 'International Fireworks Festival', 'International Film Festival', 'Montreal Beer Festival', 'Montreal Reggae Festival', 'Montreal Grand Prix', 'International Festival', 'international events', 'Laughs Festival', 'North America', 'Summer Olympics', 'successful world', '20th Century', 'vibrant scene', 'Les FrancoFolies', 'Montréal', 'Circus Arts', 'Divers/Cité Gay', 'Lesbian Pride', 'Expo', 'fair']
    temp_marks = 0
    total_marks = len(answer1)
    for i in range(len(result[0]['key_phrases'])):
        if result[0]['key_phrases'][i] in answer1:
            temp_marks += 1
    final_marks = temp_marks * 100 / total_marks

if __name__ == '__main__':
    sample_extract_key_phrases()