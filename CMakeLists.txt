cmake_minimum_required(VERSION 3.12)
project(daqdemos VERSION 1.0.0)

find_package(daq-cmake REQUIRED )

daq_setup_environment()

find_package(appfwk REQUIRED)

daq_add_plugin(ListReverser duneDAQModule	     LINK_LIBRARIES appfwk::appfwk)
daq_add_plugin(RandomDataListGenerator duneDAQModule SCHEMA LINK_LIBRARIES appfwk::appfwk)
daq_add_plugin(ReversedListValidator duneDAQModule   LINK_LIBRARIES appfwk::appfwk)

daq_add_plugin( FakeDataConsumerDAQModule duneDAQModule LINK_LIBRARIES appfwk SCHEMA)
daq_add_plugin( FakeDataProducerDAQModule duneDAQModule LINK_LIBRARIES appfwk SCHEMA)

daq_install()
