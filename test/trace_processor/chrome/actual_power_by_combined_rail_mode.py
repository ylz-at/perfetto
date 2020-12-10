#!/usr/bin/env python3
# Copyright (C) 2020 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os import sys

import synth_common

trace = synth_common.create_trace()

process_track1 = 1234
process_track2 = 4567

process_pid1 = 2345
process_pid2 = 5678

thread_track1 = 1235
thread_track2 = 4568

rail_track1 = 1236
rail_track2 = 4569

# Main threads have the same ID as the process
thread_tid1 = process_pid1
thread_tid2 = process_pid2

seq1 = 9876
seq2 = 9877

thread1_counter = 60
thread2_counter = 61

packet = trace.add_packet()
packet = trace.add_power_rails_desc(0, "PPVAR_VPH_PWR_RF")
packet = trace.add_power_rails_desc(1, "PPVAR_VPH_PWR_S1C")

trace.add_chrome_process_track_descriptor(process_track1, process_pid1)
trace.add_chrome_process_track_descriptor(process_track2, process_pid2)

trace.add_chrome_thread_with_cpu_counter(
    process_track1,
    thread_track1,
    trusted_packet_sequence_id=seq1,
    counter_track=thread1_counter,
    pid=process_pid1,
    tid=thread_tid1,
    thread_type=synth_common.CHROME_THREAD_MAIN)

trace.add_chrome_thread_with_cpu_counter(
    process_track2,
    thread_track2,
    trusted_packet_sequence_id=seq2,
    counter_track=thread2_counter,
    pid=process_pid2,
    tid=thread_tid2,
    thread_type=synth_common.CHROME_THREAD_MAIN)

trace.add_track_descriptor(rail_track1, parent=process_track1)
trace.add_track_descriptor(rail_track2, parent=process_track2)

trace.add_rail_mode_slice(
    ts=0, dur=10000000, track=rail_track1, mode=synth_common.RAIL_MODE_RESPONSE)
trace.add_rail_mode_slice(
    ts=10000000,
    dur=20000000,
    track=rail_track1,
    mode=synth_common.RAIL_MODE_LOAD)
trace.add_rail_mode_slice(
    ts=30000000, dur=-1, track=rail_track1, mode=synth_common.RAIL_MODE_IDLE)

trace.add_track_event_slice(
    "task",
    0,
    10000000,
    trusted_sequence_id=seq2,
    cpu_start=0,
    cpu_delta=10000000)

trace.add_rail_mode_slice(
    ts=0,
    dur=10000000,
    track=rail_track2,
    mode=synth_common.RAIL_MODE_ANIMATION)
trace.add_rail_mode_slice(
    ts=10000000,
    dur=25000000,
    track=rail_track2,
    mode=synth_common.RAIL_MODE_IDLE)
trace.add_rail_mode_slice(
    ts=35000000,
    dur=10000000,
    track=rail_track2,
    mode=synth_common.RAIL_MODE_ANIMATION)
trace.add_rail_mode_slice(
    ts=45000000,
    dur=10000000,
    track=rail_track2,
    mode=synth_common.RAIL_MODE_IDLE)

packet = trace.add_packet()

# cellular
packet = trace.add_power_rails_data(0, 0, 0)
packet = trace.add_power_rails_data(10, 0, 0)
packet = trace.add_power_rails_data(20, 0, 30)
packet = trace.add_power_rails_data(30, 0, 50)
packet = trace.add_power_rails_data(40, 0, 55)
packet = trace.add_power_rails_data(50, 0, 56)
packet = trace.add_power_rails_data(55, 0, 56)

# cpu little cores
packet = trace.add_power_rails_data(0, 1, 0)
packet = trace.add_power_rails_data(10, 1, 20)
packet = trace.add_power_rails_data(20, 1, 30)
packet = trace.add_power_rails_data(30, 1, 40)
packet = trace.add_power_rails_data(40, 1, 42)
packet = trace.add_power_rails_data(50, 1, 60)
packet = trace.add_power_rails_data(55, 1, 61)

sys.stdout.buffer.write(trace.trace.SerializeToString())
