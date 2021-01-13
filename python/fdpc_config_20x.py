#!/usr/bin/env python
import moo.otypes

from dunedaq.env import get_moo_model_path
moo.otypes.load_types('appfwk-cmd-schema.jsonnet', get_moo_model_path())
moo.otypes.load_types('daqdemos-FakeDataConsumerDAQModule-schema.jsonnet', get_moo_model_path())
moo.otypes.load_types('daqdemos-FakeDataProducerDAQModule-schema.jsonnet', get_moo_model_path())


import dunedaq.appfwk.cmd as cmd # AddressedCmd, 
import dunedaq.daqdemos.fakedataconsumerdaqmodule as fdc
import dunedaq.daqdemos.fakedataproducerdaqmodule as fdp

# Define modules and queues
queues = cmd.QueueSpecs(
    [
        cmd.QueueSpec(kind='FollyMPMCQueue', inst=f"hose_{i}", capacity=1000)
        for i in range(2)
    ]
)

modules = cmd.ModSpecs(
    [
        cmd.ModSpec(inst=f"fdp_{i}", plugin="FakeDataProducerDAQModule",
            data=cmd.ModInit(
                qinfos=cmd.QueueInfos([
                    cmd.QueueInfo(inst="hose_{}".format(i//10), name="output", dir="output")
                ])
            )
        )
        for i in range(20)
    ] + [
        cmd.ModSpec(inst=f"fdc_{i}", plugin="FakeDataConsumerDAQModule",
            data=cmd.ModInit(
                qinfos=cmd.QueueInfos([
                    cmd.QueueInfo(inst=f"hose_{i}", name="input", dir="input")
                ])
            )
        )
        for i in range(2)
    ]
)

# Init command
initcmd = cmd.Command(
    id=cmd.CmdId("init"),
    data=cmd.Init(queues=queues, modules=modules)
)

confcmd = cmd.Command(
    id=cmd.CmdId("conf"),
    data=cmd.CmdObj(
        modules=cmd.AddressedCmds([
            cmd.AddressedCmd(match="fdp_.*", data=fdp.Conf(
                ending_int= 14,
                nIntsPerVector= 10,
                queue_timeout_ms= 100,
                starting_int= -4,
                wait_between_sends_ms= 20000

            )),
            cmd.AddressedCmd(match="fdc_.*", data=fdc.Conf(
                ending_int = 14,
                nIntsPerVector = 10,
                queue_timeout_ms = 100,
                starting_int = -4
            ))
        ])
    )
)

startcmd = cmd.Command(
    id=cmd.CmdId('start'),
    data=cmd.CmdObj(
        modules=cmd.AddressedCmds([])
    )
)

stopcmd = cmd.Command(
    id=cmd.CmdId('stop'),
    data=cmd.CmdObj(
        modules=cmd.AddressedCmds([])
    )
)

# Create a list of commands
cmd_seq = [initcmd, confcmd, startcmd, stopcmd]

# Print them as json (to be improved/moved out)
jstr = json.dumps([c.pod() for c in cmd_seq], indent=4, sort_keys=True)
print(jstr)
with open('fdpc_config_20x.json', 'w') as f:
    f.write(jstr)

