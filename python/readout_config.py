#!/usr/bin/env python
import moo.otypes

from dunedaq.env import get_moo_model_path
moo.otypes.load_types('appfwk-cmd-schema.jsonnet', get_moo_model_path())
# moo.otypes.load_types('readout-DataLinkHandler-schema.jsonnet', get_moo_model_path())git 
# moo.otypes.load_types('readout-FelixCardReader-schema.jsonnet', get_moo_model_path())git 

import json

import dunedaq.appfwk.cmd as cmd # AddressedCmd, 
# import dunedaq.readout.datalinkhandler as ldh
# import dunedaq.readout.felixcardreader as fcr

# Define modules and queues
queues = cmd.QueueSpecs(
    [
        cmd.QueueSpec(kind='FollySPSCQueue', inst=f"linkchunks_{i}", capacity=10000)
        for i in range(10)
    ] + [
        cmd.QueueSpec(kind='FollySPSCQueue', inst=f"request_{i}", capacity=100)
        for i in range(10)
    ] + [
        cmd.QueueSpec(kind='FollySPSCQueue', inst=f"fragments_{i}", capacity=100)
        for i in range(10)
    ] + [
        cmd.QueueSpec(kind='FollyMPMCQueue', inst=f"timeinfo", capacity=100)
    ]
)
fcr_mods = xcards = [
        cmd.ModSpec(inst=f"fcr_{i}", plugin="FelixCardReader",
            data=cmd.ModInit(
                qinfos=cmd.QueueInfos([
                    cmd.QueueInfo(inst=f"linkchunks_{i*5+j}", name=f"linkdata_{j}", dir="output")
                    for j in range(5)
                ])
            )
        )
        for i in range(2)
    ]

print(fcr_mods)


dh_mods = [ 
    cmd.ModSpec(inst=f"ldh_{i}", plugin="DataLinkHandler",
        data=cmd.ModInit(
            qinfos=cmd.QueueInfos([
                cmd.QueueInfo(inst=f"linkchunks_{i}", name="linkdata", dir="input")
            ] + [
                cmd.QueueInfo(inst=f"request_{i}", name="requests", dir="input")
            ] + [
                cmd.QueueInfo(inst=f"fragments_{i}", name="fragments", dir="output")
            ] + [
                cmd.QueueInfo(inst=f"timeinfo", name="timeinfo", dir="output")
            ])
        )
    ) for i in range(10)
]

appinit = cmd.Init(queues=queues, modules=fcr_mods+dh_mods)

jstr = json.dumps(appinit.pod(), indent=4, sort_keys=True)
print(jstr)

# # Init command
# initcmd = cmd.Command(
#     id=cmd.CmdId("init"),
#     data=cmd.Init(queues=queues, modules=modules)
# )

# confcmd = cmd.Command(
#     id=cmd.CmdId("conf"),
#     data=cmd.CmdObj(
#         modules=cmd.AddressedCmds([
#             cmd.AddressedCmd(match="fcr_{i}", data=fcr.ConfParams(
#                 card_id= 0,
#                 card_offset= {i},
#                 dma_id= {i},
#                 numa_id= {i},
#                 num_sources= 5

#             ))
#             for i in range(2)
#             ] + [
#             cmd.AddressedCmd(match="ldh_.*", data=ldh.ConfParams(
#                 raw_type = "wib",
#                 source_queue_timeout_ms = 2000,
#                 latency_buffer_size = 100000,
#                 pop_limit_pct = 0.5,
#                 pop_size_pct = 0.8
#             ))
#         ])
#     )
# )

# startcmd = cmd.Command(
#     id=cmd.CmdId('start'),
#     data=cmd.CmdObj(
#         modules=cmd.AddressedCmds([])
#     )
# )

# stopcmd = cmd.Command(
#     id=cmd.CmdId('stop'),
#     data=cmd.CmdObj(
#         modules=cmd.AddressedCmds([])
#     )
# )

# # Create a list of commands
# cmd_seq = [initcmd, confcmd, startcmd, stopcmd]

# # Print them as json (to be improved/moved out)
# jstr = json.dumps([c.pod() for c in cmd_seq], indent=4, sort_keys=True)
# print(jstr)
# with open('readout_config.json', 'w') as f:
#     f.write(jstr)

