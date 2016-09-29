#!/usr/bin/env python
# coding=utf-8
from django.contrib import admin

from .models import Question,Choice

# 添加选项, 通过改变 TabularInline 对应的值，可以改变样式
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


# 改变管理页面的某些选项
class QuestionAdmin(admin.ModelAdmin):
    # 修改了表单中字段的顺序
    # fields = ['pub_date', 'question_text']
    fieldsets = [
        (None, {'fields': ['question_text']}),
        # 第一个元素是分组名
        ('Date information', {'fields': ['pub_date']}),
    ]
    # 为问题添加选项
    inlines = [ChoiceInline]
    # 在问题列表里，被显示的字段名
    list_display = ('question_text', 'pub_date')
    # 过滤条件
    list_filter = ['pub_date']
    # 搜索功能
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)