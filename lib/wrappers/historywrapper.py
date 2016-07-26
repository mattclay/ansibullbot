#!/usr/bin/env python

import os
import sys
import time
from datetime import datetime
from operator import itemgetter

# historywrapper.py
#
#   HistoryWrapper - a tool to ask questions about an issue's history
#
#   This class will join the events and comments of an issue into
#   an object that allows the user to make basic queries without
#   having to iterate through events manaully. 
#
#   Constructor Examples:
#       hwrapper = HistoryWrapper(IssueWrapper)
#       hwrapper = HistoryWrapper(PullRequestWrapper)
#
#   https://developer.github.com/v3/issues/events/
#   https://developer.github.com/v3/issues/comments/

class HistoryWrapper(object):

    def __init__(self, issue):
        self.issue = issue
        self.history = self.process()

    def _find_events_by_actor(self, event, actor, maxcount=1):
        matching_events = []
        for event in self.history:
            if event['event'] == 'referenced' and event['actor'] == username:
                matching_events.append(event)
                if len(matching_events) == maxcount:
                    break
        return matching_events

    def is_referenced(self, username):
        matching_events = self._find_events_by_actor('referenced', username)
        if len(matching_events) > 0:
            return True
        else:
            return False

    def is_mentioned(self, username):
        matching_events = self._find_events_by_actor('mentioned', username)
        if len(matching_events) > 0:
            return True
        else:
            return False

    def has_subscribed(self, username):
        matching_events = self._find_events_by_actor('subscribed', username)
        if len(matching_events) > 0:
            return True
        else:
            return False

   def was_assigned(self, username):
        matching_events = self._find_events_by_actor('assigned', username)
        if len(matching_events) > 0:
            return True
        else:
            return False

   def was_unassigned(self, username):
        matching_events = self._find_events_by_actor('unassigned', username)
        if len(matching_events) > 0:
            return True
        else:
            return False

   def was_subscribed(self, username):
        matching_events = self._find_events_by_actor('subscribed', username)
        if len(matching_events) > 0:
            return True
        else:
            return False

   def was_labeled(self, label=None):
        """Were labels -ever- applied to this issue?"""
        labeled = False
        for event in self.history:
            if event['event'] == 'labeled':
                if label and event['label'] == label:
                    labeled = True
                    break
                elif not label:
                    labeled = True
                    break
        return labeled

   def was_unlabeled(self, label=None):
        """Were labels -ever- unapplied from this issue?"""
        labeled = False
        for event in self.history:
            if event['event'] == 'unlabeled':
                if label and event['label'] == label:
                    labeled = True
                    break
                elif not label:
                    labeled = True
                    break
        return labeled

    def process(self):
        events = self.issue.get_events()
        comments = self.issue.get_comments()
        today = datetime.today()

        processed_events = []
        for ide,event in enumerate(events):
            edict = {}
            edict['id'] = event.id
            edict['actor'] = event.actor.login
            edict['event'] = event.event
            edict['created_at'] = event.created_at
            raw_data = event.raw_data.copy()
            if edict['event'] in ['labeled', 'unlabeled']:
                edict['label'] = raw_data.get('label', {}).get('name', None)
            elif edict['event'] == 'mentioned':
                pass
            elif edict['event'] == 'subscribed':
                pass
            elif edict['event'] == 'referenced':
                edict['commit_id'] = event.commit_id
            processed_events.append(edict)

        for idc,comment in enumerate(comments):
            edict['id'] = comment.id
            edict['event'] = 'commented'
            edict['actor'] = comment.user.login
            edict['created_at'] = comment.created_at
            edict['body'] = comment.body
            if edict not in processed_events:
                processed_events.append(edict)

        # sort by created_at
        sorted_events = sorted(processed_events, key=itemgetter('created_at')) 

        # return ...
        return sorted_events

