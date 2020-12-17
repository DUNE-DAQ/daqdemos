import mootools
import json

mootools.import_schema('appfwk-cmd-schema.jsonnet')
mootools.import_schema('daqdemos-FakeDataConsumerDAQModule-schema.jsonnet')
mootools.import_schema('daqdemos-FakeDataProducerDAQModule-schema.jsonnet')


import dunedaq.appfwk.cmd as cmd # AddressedCmd, 
import dunedaq.daqdemos.fakedataconsumerdaqmodule as fdc
import dunedaq.daqdemos.fakedataproducerdaqmodule as fdp

# Define modules and queues
queues = cmd.QueueSpecs([
  cmd.QueueSpec(kind='StdDeQueue', inst="hose", capacity=10)
])

modules = cmd.ModSpecs([
  cmd.ModSpec(inst="source", plugin="FakeDataProducerDAQModule",
    data=cmd.QueueInfo(inst="hose", name="output", dir="output")),
  cmd.ModSpec(inst="sink", plugin="FakeDataConsumerDAQModule",
    data=cmd.QueueInfo(inst="host", name="input", dir="input"))])

# Init command
initcmd = cmd.Command(
    id=cmd.CmdId("init"),
    data=cmd.Init(queues=queues, modules=modules)
)

confcmd = cmd.Command(
    id=cmd.CmdId("conf"),
    data=cmd.CmdObj(
        modules=cmd.AddressedCmds([
            cmd.AddressedCmd(match="fdp", data=fdp.Conf(
                ending_int= 14,
                nIntsPerVector= 10,
                queue_timeout_ms= 100,
                starting_int= -4,
                wait_between_sends_ms= 1000

            )),
            cmd.AddressedCmd(match="fdc", data=fdc.Conf(
                ending_int = 14,
                nIntsPerVector = 10,
                queue_timeout_ms = 100,
                starting_int = -4
            ))
        ])
    )
)

startcmd = cmd.Command(
    id=cmd.CmdId('start')
)

stopcmd = cmd.Command(
    id=cmd.CmdId('stop')
)

# Create a list of commands
cmd_seq = [initcmd, confcmd, startcmd, stopcmd]

# Print them as json (to be improved/moved out)
print(json.dumps([c.pod() for c in cmd_seq], indent=4, sort_keys=True))