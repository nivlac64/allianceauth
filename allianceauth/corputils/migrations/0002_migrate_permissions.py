# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-14 21:48
from __future__ import unicode_literals

from django.db import migrations

PERMISSIONS = {
    'user': [
        'corp_apis',
        'alliance_apis',
    ],
    'corpstats': {
        'corp_apis': 'Can view API keys of members of their corporation.',
        'alliance_apis': 'Can view API keys of members of their alliance.',
        'blue_apis': 'Can view API keys of members of blue corporations.',
        'view_corp_corpstats': 'Can view corp stats of their corporation.',
        'view_alliance_corpstats': 'Can view corp stats of members of their alliance.',
        'view_blue_corpstats': 'Can view corp stats of blue corporations.',
    }
}


def user_permissions_dict(apps):
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    User = apps.get_model('auth', 'User')
    CorpStats = apps.get_model('corputils', 'CorpStats')

    user_ct = ContentType.objects.get_for_model(User)
    corpstats_ct = ContentType.objects.get_for_model(CorpStats)

    return {
        'user': {x: Permission.objects.get_or_create(name=x, codename=x, content_type=user_ct)[0] for x in PERMISSIONS['user']},
        'corpstats': {x: Permission.objects.get_or_create(codename=x, name=y, content_type=corpstats_ct)[0] for x, y in PERMISSIONS['corpstats'].items()},
    }


def users_with_permission(apps, perm):
    User = apps.get_model('auth', 'User')
    return User.objects.filter(user_permissions=perm.pk)


def groups_with_permission(apps, perm):
    Group = apps.get_model('auth', 'Group')
    return Group.objects.filter(permissions=perm.pk)


def forward(apps, schema_editor):
    perm_dict = user_permissions_dict(apps)

    corp_users = users_with_permission(apps, perm_dict['user']['corp_apis'])
    for u in corp_users:
        u.user_permissions.add(perm_dict['corpstats']['corp_apis'].pk)
        u.user_permissions.add(perm_dict['corpstats']['view_corp_corpstats'].pk)

    alliance_users = users_with_permission(apps, perm_dict['user']['alliance_apis'])
    for u in alliance_users:
        u.user_permissions.add(perm_dict['corpstats']['alliance_apis'].pk)
        u.user_permissions.add(perm_dict['corpstats']['view_alliance_corpstats'].pk)

    corp_groups = groups_with_permission(apps, perm_dict['user']['corp_apis'])
    for g in corp_groups:
        g.permissions.add(perm_dict['corpstats']['corp_apis'].pk)
        g.permissions.add(perm_dict['corpstats']['view_corp_corpstats'].pk)

    alliance_groups = groups_with_permission(apps, perm_dict['user']['alliance_apis'])
    for g in alliance_groups:
        g.permissions.add(perm_dict['corpstats']['alliance_apis'].pk)
        g.permissions.add(perm_dict['corpstats']['view_alliance_corpstats'].pk)

    for name, perm in perm_dict['user'].items():
        perm.delete()


def reverse(apps, schema_editor):
    perm_dict = user_permissions_dict(apps)

    corp_users = users_with_permission(apps, perm_dict['corpstats']['view_corp_corpstats'])
    corp_api_users = users_with_permission(apps, perm_dict['corpstats']['corp_apis'])
    corp_us = corp_users | corp_api_users
    for u in corp_us.distinct():
        u.user_permissions.add(perm_dict['user']['corp_apis'].pk)
    for u in corp_users:
        u.user_permissions.remove(perm_dict['corpstats']['view_corp_corpstats'].pk)
    for u in corp_api_users:
        u.user_permissions.remove(perm_dict['corpstats']['corp_apis'].pk)

    alliance_users = users_with_permission(apps, perm_dict['corpstats']['view_alliance_corpstats'])
    alliance_api_users = users_with_permission(apps, perm_dict['corpstats']['alliance_apis'])
    alliance_us = alliance_users | alliance_api_users
    for u in alliance_us.distinct():
        u.user_permissions.add(perm_dict['user']['alliance_apis'].pk)
    for u in alliance_users:
        u.user_permissions.remove(perm_dict['corpstats']['view_alliance_corpstats'].pk)
    for u in alliance_api_users:
        u.user_permissions.remove(perm_dict['corpstats']['alliance_apis'].pk)

    corp_groups = groups_with_permission(apps, perm_dict['corpstats']['view_corp_corpstats'])
    corp_api_groups = groups_with_permission(apps, perm_dict['corpstats']['corp_apis'])
    for g in corp_groups.distinct():
        g.permissions.add(perm_dict['user']['corp_apis'].pk)
    for g in corp_groups:
        g.permissions.remove(perm_dict['corpstats']['view_corp_corpstats'].pk)
    for g in corp_api_groups:
        g.permissions.remove(perm_dict['corpstats']['corp_apis'].pk)

    alliance_groups = groups_with_permission(apps, perm_dict['corpstats']['view_alliance_corpstats'])
    alliance_api_groups = groups_with_permission(apps, perm_dict['corpstats']['alliance_apis'])
    alliance_gs = alliance_groups | alliance_api_groups
    for g in alliance_gs.distinct():
        g.permissions.add(perm_dict['user']['alliance_apis'].pk)
    for g in alliance_groups:
        g.permissions.remove(perm_dict['corpstats']['view_alliance_corpstats'].pk)
    for g in alliance_api_groups:
        g.permissions.remove(perm_dict['corpstats']['alliance_apis'].pk)


class Migration(migrations.Migration):

    dependencies = [
        ('corputils', '0001_initial'),
        ('authentication', '0005_delete_perms'),
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.RunPython(forward, reverse),
    ]