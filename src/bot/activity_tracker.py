# General
import datetime as dt

# Library
import nextcord


def get_activity(member: nextcord.Member) -> dict:
    '''
    Returns a dictionary of the member's activity data.

    :param member: The member object to get activity data from.
    '''
    # Basic info
    user_id = member.id
    username = member.name
    status = str(member.status)

    # Voice activity
    voice_activity = member.voice

    # Activity info
    activity = member.activity

    if isinstance(activity, nextcord.activity.Game):
        activity = {'Game': activity.name}
    elif isinstance(activity, nextcord.activity.Streaming):
        activity = {'Streaming': activity.game}
    elif isinstance(activity, nextcord.activity.CustomActivity):
        activity = {'CustomActivity': activity.name}
    else:
        activity = {'None': None}

    # Compile the data
    data = {
        'user_id': user_id,
        'username': username,
        'status': status,
        'activity': activity,
        'voice_activity': voice_activity
    }

    return data


def get_guild_activity(date: dt.datetime, guild: nextcord.Guild) -> list:
    member_data = []

    for member in guild.members:
        data = get_activity(member)
        data['timestamp'] = date

        member_data.append(data)

    return member_data
