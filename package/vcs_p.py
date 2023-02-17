#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

#  Artem Smirnov by Promobot
#  TODO: to add auto complete function 
# see https://kislyuk.github.io/argcomplete


import parse_args as pa
import work_functions as wa
import config_func as cf


def parse_work():
    args = pa.parse_args()

    if args.clear:
        wa.work_clear()

    if args.init:
        wa.work_init()

    if not cf.init_repos_json():
        return

    print("\nSync started... \n\n")
    wa.work_sync()
    print("\nSync completed! Working on direct command... \n\n")

    if pa.__ch_str(args.orep):
        wa.work_orep(args.orep)

    if args.oallrepos:
        wa.work_oallrepos()

    if pa.__ch_str(args.profile):
        wa.work_add_profile(args.profile)

    if pa.__ch_str(args.checkoutb):
        wa.work_checkoutb(args.checkoutb)

    if pa.__ch_str(args.checkout):
        wa.work_checkout(args.checkout)

    if pa.__ch_str(args.cfgb):
        cf.__switch_branch_cfg(args.cfgb)

    if args.show_repos:
        wa.work_show_repos()

    if args.fetch:
        wa.work_fetch()

    if args.status:
        wa.work_status()

    if args.pull:
        wa.work_pull()

    if args.push:
        wa.work_push()

    if args.sync:
        wa.work_sync()

    if args.add:
        wa.work_add()

    if args.commit:
        wa.work_commit()


parse_work()
exit(0)
