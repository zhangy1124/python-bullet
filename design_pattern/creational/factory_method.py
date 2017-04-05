# -*- coding: utf-8 -*-

"""
Factory Method Pattern


Real world example

Consider the case of a hiring manager. It is impossible for one person to 
interview for each of the positions. Based on the job opening, she has to 
decide and delegate the interview steps to different people.


In plain words

It provides a way to delegate the instantiation logic to child classes.


Wikipedia says

In class-based programming, the factory method pattern is a creational pattern
that uses factory methods to deal with the problem of creating objects without
having to specify the exact class of the object that will be created. This is
done by creating objects by calling a factory method—either specified in an
interface and implemented by child classes, or implemented in a base class 
and optionally overridden by derived classes—rather than by calling a
constructor.


When to use?

Useful when there is some generic processing in a class but the required 
sub-class is dynamically decided at runtime. Or putting it in other words, 
when the client doesn't know what exact sub-class it might need.
"""


class Interviewer(object):
    def ask_questions(self):
        raise NotImplementedError()


class Developer(Interviewer):
    def ask_questions(self):
        print('Asking about design patterns!')


class CommunityExecutive(Interviewer):
    def ask_questions(self):
        print('Asking about community building')


class HiringManager(object):
    def make_interviewer(self):
        raise NotImplementedError()

    def take_interview(self):
        interviewer = self.make_interviewer()
        interviewer.ask_questions()


class DevelopmentManager(HiringManager):
    def make_interviewer(self):
        return Developer()


class MarketingManager(HiringManager):
    def make_interviewer(self):
        return CommunityExecutive()


# usage

develop_manager = DevelopmentManager()
develop_manager.take_interview()

marketing_manager = MarketingManager()
marketing_manager.take_interview()
