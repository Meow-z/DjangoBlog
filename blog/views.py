#!/usr/bin/env python
# coding=utf-8
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Choice, Question

# 视图的作用 1) 返回 HttpResponse 对象 2）抛出异常
# 模板填充 1)from django.template import loader
#           template = loader.get_template('blog/index.html')
#           return HttpResponse(template.render(context, request))
#          2)from django.shortcuts import render
#           return render(request, 'blog/index.html', context)
# 抛出异常  1） from django.http import Http404
#               try:
#                   question = Question.objects.get(pk=question_id)
#               except Question.DoesNotExist:
#                   raise Http404("Question does not exist")
#           2)  from django.shortcuts import get_object_or_404
#               question = get_object_or_404(Question, pk=question_id)
# 数据库读取记录    from .models import Question
#                   1) latest_question_list = Question.objects.order_by('-pub_date')[:5]
#                   2) question = Question.objects.get(pk=question_id)
#                   3) question = Question.objects.filter(pk=question_id)
#                   4) question = get_object_or_404(Question, pk=question_id)
#                   5) question = get_list_or_404(Question, pk=question_id)
class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """返回最后发布的5个问题"""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'blog/detail.html'



class ResultsView(generic.DetailView):
    model = Question
    template_name = 'blog/results.html'

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST['choice'] 以字符串形式返回选择的 Choice 的 ID
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 重新显示问题的投票表单
        return render(request, 'blog/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 成功处理之后 POST 数据之后，总是返回一个 HttpResponseRedirect 。防止因为用户点击了后退按钮而提交了两次。
        return HttpResponseRedirect(reverse('blog:results', args=(p.id,)))