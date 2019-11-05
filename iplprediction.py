#!/usr/bin/env python
# coding: utf-8

# In[107]:


import pandas
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np

deliveries_df = pandas.read_csv('~/Desktop/ipl/deliveries.csv')
matches_df = pandas.read_csv('~/Desktop/ipl/matches.csv')

total_matches = matches_df.loc[(matches_df['team1'] == 'Sunrisers Hyderabad' ) 
                               & (matches_df['team2'] == 'Royal Challengers Bangalore')].count()

winning_count = matches_df.loc[(matches_df['team1'] == 'Sunrisers Hyderabad' ) 
               & (matches_df['team2'] == 'Royal Challengers Bangalore')
               & (matches_df['winner'] == 'Royal Challengers Bangalore')].count()

total_teams_data = deliveries_df.loc[((deliveries_df['batting_team']  == 'Sunrisers Hyderabad') 
                               & (deliveries_df['bowling_team'] == 'Royal Challengers Bangalore')) |
                              ((deliveries_df['bowling_team']  == 'Sunrisers Hyderabad') 
                               & (deliveries_df['batting_team'] == 'Royal Challengers Bangalore'))]

first_team_data = deliveries_df.loc[(deliveries_df['batting_team']  == 'Sunrisers Hyderabad')]

second_team_data = deliveries_df.loc[(deliveries_df['batting_team']  == 'Royal Challengers Bangalore')] 

#Grouped By on the basis of match Id

grouped_data = total_teams_data.groupby(['match_id' ]).first()

batsman_data =  total_teams_data.loc[(total_teams_data['batsman'] == 'DA Warner') 
                                   & (total_teams_data['match_id'] == 1)]

total_batsman_name = total_teams_data['batsman'].unique() 

#getting the Batsman record

batsman_record=[];
for batsman in total_batsman_name:
    player_record = total_teams_data.loc[total_teams_data['batsman'] == batsman]
    batsman_record.append({
        'name' : batsman,
        'total_run': sum(player_record['batsman_runs'])
    })

# DataFram for the batsman Record with the total runs    

new_Dataframe = DataFrame(data=batsman_record , index =total_batsman_name )

#Plotting Graph for batsman Dataframe

new_Dataframe.plot(kind='bar' , figsize=(14,8),title="Total runs earned by the batsman")

#Calculating the best 10 Batsman on the basis of runs

top_batsman_list = new_Dataframe.nlargest(10, 'total_run')

#Unique list of bowlers

total_bowlers_name =  total_teams_data['bowler'].unique()

#Getting the bowlers record

bowlers_record=[];
for bowler in total_bowlers_name:
    player_record = total_teams_data.loc[(total_teams_data['bowler'] == bowler ) 
                                        & (total_teams_data['player_dismissed'].notnull())]
    counts = player_record.count()
    bowlers_record.append({
        'name' : bowler,
        'total_wickets': counts['bowler']
    })

#DataFrame for Bowler's record
    
new_Dataframe = DataFrame(data=bowlers_record , index =total_bowlers_name )

#Plotting the Graph for Bowler's Records along with the wickets

new_Dataframe.plot(kind='bar' , figsize=(14,8),title="Total wicket taken by the bowlers")

#Top 10 bowlers list 

top_bowlers_list = new_Dataframe.nlargest(10, 'total_wickets')


# ## Plotting Graph for the top 10 batsman's record

# In[112]:



list_top_bowlers = top_bowlers_list['name'].tolist()
list_top_batsman = top_batsman_list['name'].tolist()
batsman_out_record = [];
batsman_record_with_dismissal_kind =[]
batsman_record_six_four = []
unique_dataset_dismissal_kind =total_teams_data['dismissal_kind'].unique()

for batsman in list_top_batsman:
    batsman_records_six = total_teams_data.loc[(total_teams_data['batsman'] == batsman) &
                                               (total_teams_data['batsman_runs'] == 6)].count()
    batsman_record_six_four.append({
        'player-name' :batsman,
        'type' : 'six',
        'count' : batsman_records_six['batsman_runs']
    })
    batsman_records_four = total_teams_data.loc[(total_teams_data['batsman'] == batsman) & 
                                                (total_teams_data['batsman_runs'] == 4)].count()
    batsman_record_six_four.append({
        'player-name' :batsman,
        'type' : 'Four',
        'count' : batsman_records_four['batsman_runs']
    })
    for bowler in total_bowlers_name:
        batsman_records = total_teams_data.loc[(total_teams_data['player_dismissed'] == batsman) 
                                               & (total_teams_data['bowler'] == bowler)]
        count = batsman_records.count()
        batsman_out_record.append({
            'batsman_name' : batsman , 
            'bowler_name'  : bowler ,
            'count' : count['bowler']
        })
    for dismissal in unique_dataset_dismissal_kind:
        batsman_records = total_teams_data.loc[(total_teams_data['player_dismissed'] == batsman) 
                                               & (total_teams_data['dismissal_kind'] == dismissal)]
        count = batsman_records.count()
        batsman_record_with_dismissal_kind.append({
             'player_dismissed': batsman,
             'dismissed-type' : dismissal,
             'count' : count['player_dismissed']
         })


#Data frame of Record top 10 bowlers and top 10 batsman Relation

new_Dataframe = DataFrame(data=batsman_out_record)

#Data frame top 10 batsman along with their dimissal kind

batsman_record_with_dismissal_kind_dataframe = DataFrame(data=batsman_record_with_dismissal_kind)

#Data frame top 10 batsman along with the sixes and four 

batsman_record_with_six_four_dataframe = DataFrame(data=batsman_record_six_four)

#plotting Graph for every batsman

for batsman in list_top_batsman:
    batsman_record = new_Dataframe.loc[(new_Dataframe['batsman_name'] == batsman )]
    batsman_record.index = batsman_record['bowler_name']
    batsman_record.plot(kind='bar' , figsize=(14,8),title=batsman)
    
#Plotting the Graph of top 10 batsman along with their dimissal kind
    
    batsman_record_dimissal_kind = batsman_record_with_dismissal_kind_dataframe.loc[(
        batsman_record_with_dismissal_kind_dataframe['player_dismissed'] == batsman )]
    batsman_record_dimissal_kind.index = batsman_record_dimissal_kind['dismissed-type']
    batsman_record_dimissal_kind.plot(kind='bar' , figsize=(14,8),title=batsman)
    
#Plottind the Graph top 10 batsman along with the sixes and four   
    
    batsman_record_four_six = batsman_record_with_six_four_dataframe.loc[(
        batsman_record_with_six_four_dataframe['player-name'] == batsman )]
    batsman_record_four_six.index = batsman_record_four_six['type']
    batsman_record_four_six.plot(kind='bar' , figsize=(14,8),title=batsman)
    

    
                                       


# ## PartnerShip Record helps you to choose the batting order of your team.

# In[109]:


partnership_records = []
for batsman in list_top_batsman:
    for non_striker in total_batsman_name:
        if(batsman != non_striker):
            batsman_non_striker_record = total_teams_data.loc[((total_teams_data['non_striker'] 
                                                                          == non_striker)  
                                                                        & (total_teams_data['batsman'] == batsman)) 
                                                                        | ((total_teams_data['non_striker'] 
                                                                          == batsman)  
                                                                        & (total_teams_data['batsman'] 
                                                                           == non_striker)) ]
            partnership_records.append({
                'non-striker' : non_striker,
                'batsman'  : batsman ,
                'total_run'  : sum(batsman_non_striker_record['total_runs'])
            })
        
        
#Dataframe for the Partnership Record
        
batsman_record_with_six_four_dataframe = DataFrame(data=partnership_records ,
                                                   columns=['non-striker', 'batsman', 'total_run'])

for batsman in list_top_batsman:
    batsman_partnership_record_dataframe_one = batsman_record_with_six_four_dataframe.loc[
        (batsman_record_with_six_four_dataframe['batsman'] == batsman )]

#Plotting Scatter Graph     
    
    plt.figure(figsize=(20, 5))
    
    plt.scatter(batsman_partnership_record_dataframe_one['non-striker'],
                batsman_partnership_record_dataframe_one['total_run'] , alpha=0.9)
    
    plt.xticks(rotation='vertical')
    
#To show the Scatter Graph

    plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




