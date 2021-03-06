/**
 * @file FakeDataProducerDAQModule.hpp
 *
 * FakeDataProducerDAQModule creates vectors of integers of a given length, starting with the given start integer and
 * counting up to the given ending integer. Its current position is persisted between generated vectors, so if the
 * parameters are chosen correctly, the generated vectors will "walk" through the valid range.
 *
 * This is part of the DUNE DAQ Application Framework, copyright 2020.
 * Licensing/copyright details are in the COPYING file that you should have
 * received with this code.
 */

#ifndef APPFWK_TEST_FAKEDATAPRODUCERDAQMODULE_HPP_
#define APPFWK_TEST_FAKEDATAPRODUCERDAQMODULE_HPP_

#include "appfwk/DAQModule.hpp"
#include "appfwk/DAQSink.hpp"
#include "appfwk/ThreadHelper.hpp"

// Our command structures.  
#include "daqdemos/fakedataproducerdaqmodule/Structs.hpp"

#include <future>
#include <memory>
#include <string>
#include <vector>

namespace dunedaq {
namespace fdpc {
/**
 * @brief FakeDataProducerDAQModule creates vectors of ints and sends them
 * downstream
 */
class FakeDataProducerDAQModule : public appfwk::DAQModule
{
public:
  /**
   * @brief FakeDataProducerDAQModule Constructor
   * @param name Instance name for this FakeDataProducerDAQModule instance
   */
  explicit FakeDataProducerDAQModule(const std::string& name);

  FakeDataProducerDAQModule(const FakeDataProducerDAQModule&) =
    delete; ///< FakeDataProducerDAQModule is not copy-constructible
  FakeDataProducerDAQModule& operator=(const FakeDataProducerDAQModule&) =
    delete; ///< FakeDataProducerDAQModule is not copy-assignable
  FakeDataProducerDAQModule(FakeDataProducerDAQModule&&) =
    delete; ///< FakeDataProducerDAQModule is not move-constructible
  FakeDataProducerDAQModule& operator=(FakeDataProducerDAQModule&&) =
    delete; ///< FakeDataProducerDAQModule is not move-assignable

  void init(const nlohmann::json& ) override;

private:
  // Commands
  void do_configure(const data_t& data);
  void do_start(const data_t& data);
  void do_stop(const data_t& data);

  // Threading
  appfwk::ThreadHelper thread_;
  void do_work(std::atomic<bool>& running_flag);

  // Configuration
  std::unique_ptr<appfwk::DAQSink<std::vector<int>>> outputQueue_;
  std::chrono::milliseconds queueTimeout_;

  daqdemos::fakedataproducerdaqmodule::Conf cfg_;

  // size_t nIntsPerVector_ = 999;
  // int starting_int_ = -999;
  // int ending_int_ = -999;
  // size_t wait_between_sends_ms_ = 999;
};
} // namespace appfwk

ERS_DECLARE_ISSUE_BASE(fdpc,
                       ProducerProgressUpdate,
                       appfwk::GeneralDAQModuleIssue,
                       message,
                       ((std::string)name),
                       ((std::string)message))
} // namespace dunedaq

#endif // APPFWK_TEST_FAKEDATAPRODUCERDAQMODULE_HPP_
