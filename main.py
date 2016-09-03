#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import jinja2
import webapp2
import sys
from models import Planner

reload(sys)
sys.setdefaultencoding("utf8")

template_dir = os.path.join(os.path.dirname(__file__), "html")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        list = Planner.query().fetch()
        params = {"table": list}
        return self.render_template("index.html", params=params)

    def post(self):
        date = self.request.get("year") + "-" + self.request.get("month") + "-" + self.request.get("day")
        task = self.request.get("task")
        task_save = Planner(date=date, task=task)
        task_save.put()
        return self.redirect_to("main-page")

class TaskHandler(BaseHandler):
    def get(self, task_id):
        task = Planner.get_by_id(int(task_id))
        params = {"task": task}
        return self.render_template("task.html", params=params)

class EditTask(BaseHandler):
    def post(self, task_id):
        new_date = self.request.get("date")
        new_task = self.request.get("task")
        old_task = Planner.get_by_id(int(task_id))
        old_task.date = new_date
        old_task.task = new_task
        old_task.put()
        return self.redirect_to("main-page")

class TaskCompleted(BaseHandler):
    def post(self, task_id):
        task = Planner.get_by_id(int(task_id))
        task.completed = "DA"
        task.put()
        return self.redirect_to("main-page")

class DeleteTask(BaseHandler):
    def post(self, task_id):
        task = Planner.get_by_id(int(task_id))
        task.key.delete()
        return self.redirect_to("main-page")


app = webapp2.WSGIApplication([
    webapp2.Route("/", MainHandler),
    webapp2.Route("/", MainHandler, name="main-page"),
    webapp2.Route("/<task_id:\d+>", TaskHandler),
    webapp2.Route("/<task_id:\d+>/edit", EditTask),
    webapp2.Route("/<task_id:\d+>/completed", TaskCompleted),
    webapp2.Route("/<task_id:\d+>/delete", DeleteTask),
], debug=True)
