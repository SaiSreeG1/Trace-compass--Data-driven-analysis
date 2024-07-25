import json
import xml.etree.ElementTree as ET

# Define the XML and prompts mapping (example)
prompts_xml_mapping = {
    "With a trace containing 'auth failure' events, plot the number of times a user id failed to connect vs time.": '''<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="../../org.eclipse.tracecompass.tmf.analysis.xml.core/src/org/eclipse/tracecompass/tmf/analysis/xml/core/module/xmlDefinition.xsd">
    <stateProvider version="0" id="ssh.failed.connections">
        <head>
            <traceType id="custom.txt.trace:Syslog:OpenSSHD" />
            <label value="Failed connections" />
        </head>
        <eventHandler eventName="AUTH FAILURE">
            <stateChange>
                <stateAttribute type="eventField" value="UserID" />
                <stateAttribute type="eventField" value="Message" />
                <stateValue type="int" value="1" increment="true" />
            </stateChange>
            <stateChange>
                <stateAttribute type="eventField" value="UserID" />
                <stateValue type="int" value="1" increment="true" />
            </stateChange>
        </eventHandler>
    </stateProvider>
    <xyView id="failed.connections">
        <head>
            <analysis id="ssh.failed.connections" />
            <label value="Failed Connections" />
        </head>
        <entry path="*" displayType="delta">
            <display type="self" />
        </entry>
    </xyView>
    </tmfxml>''',
    "Given the state system plot the user bandwidth, it is every attribute under the user/* branch.":'''<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="../../org.eclipse.tracecompass.tmf.analysis.xml.core/src/org/eclipse/tracecompass/tmf/analysis/xml/core/module/xmlDefinition.xsd">
    <xyView id="endpoint.bandwidth">
        <head>
            <analysis id="org.eclipse.tracecompass.incubator.internal.system.core.analsysis.httpd.HttpdConnectionAnalysis" />
            <label value="Endpoint Bandwidth" />
        </head>
        <entry path="endpoint/*"
               displayType="delta">
            <display type="self" />
        </entry>
    </xyView>
    <xyView id="ip.bandwidth">
        <head>
            <analysis id="org.eclipse.tracecompass.incubator.internal.system.core.analsysis.httpd.HttpdConnectionAnalysis" />
            <label value="IP Bandwidth" />
        </head>
        <entry path="ip/*"
               displayType="delta">
            <display type="self" />
        </entry>
    </xyView>
    <xyView id="user.bandwidth">
        <head>
            <analysis id="org.eclipse.tracecompass.incubator.internal.system.core.analsysis.httpd.HttpdConnectionAnalysis" />
            <label value="User Bandwidth" />
        </head>
        <entry path="user/*"
               displayType="delta">
            <display type="self" />
        </entry>
    </xyView>
</tmfxml>''',
    "Give me statistics on GC durations using the field Pause and classifying by type.":'''<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <pattern version="1"
             id="system.gc.duration">
        <head>
            <label value="GC Segments" />
        </head>
        <patternHandler>
            <action id="segment_create">
                <segment>
                    <segType>
                        <segName>
                            <stateValue type="eventField"
                                        value="Cause" />
                        </segName>
                    </segType>
                    <segTime>
                        <begin type="eventField"
                               value="timestamp" />
                        <duration type="eventField"
                                  value="Pause" />
                    </segTime>
                </segment>
            </action>
            <fsm id="gcs"
                 multiple="true">
                <state id="start">
                    <transition event="*"
                                target="duration"
                                action="segment_create" />
                </state>
                <final id="duration" />
            </fsm>
        </patternHandler>
    </pattern>
</tmfxml>''',
    "Analyze futex contention with a detailed state machine using the futex.h definitions. Include conditions, transitions, segment creations, and visualize scenarios over time. Plot the uaddr vs waiter and show different states like WAIT, IN_PROGRESS, MATCHED, and ABANDONED in a timegraph view.":'''<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <!-- Timegraph view for uaddr x TID -->
    <timeGraphView id="lttng2.kernel.core.futex.uaddrvswaiter">
        <head>
            <analysis id="lttng.analysis.futex" />
            <label value="Uaddr vs Waiter" />
        </head>
        <definedValue name="WAIT"
                      value="1"
                      color="#646464" />
        <entry path="lock/*">
            <display type="self" />
            <entry path="*">
                <display type="self" />
            </entry>
        </entry>
    </timeGraphView>
    <!-- Timegraph view that show the scenario execution state in time -->
    <timeGraphView id="lttng2.kernel.core.futex.scenarios">
        <head>
            <analysis id="lttng.analysis.futex" />
            <label value="Scenarios" />
        </head>
        <!-- FFA040 -->
        <definedValue name="PENDING"
                      value="0"
                      color="#CCCCCC" />
        <definedValue name="IN_PROGRESS"
                      value="1"
                      color="#00CCFF" />
        <definedValue name="MATCHED"
                      value="2"
                      color="#118811" />
        <definedValue name="ABANDONED"
                      value="3"
                      color="#EE0000" />
        <!-- Scenario view -->
        <entry path="scenarios/*">
            <display type="self" />
            <name type="self" />
            <entry path="*">
                <display type="constant"
                         value="status" />
                <name type="self" />
            </entry>
        </entry>
    </timeGraphView>
    <pattern version="0"
             id="lttng.analysis.futex">
        <head>
            <traceType id="org.eclipse.linuxtools.lttng2.kernel.tracetype" />
            <label value="Futex Contention Analysis" />
            <viewLabelPrefix value="Contention" />
        </head>
        <location id="CurrentCPU">
            <stateAttribute type="constant"
                            value="CPUs" />
            <stateAttribute type="eventField"
                            value="cpu" />
        </location>
        <location id="CurrentThread">
            <stateAttribute type="location"
                            value="CurrentCPU" />
            <stateAttribute type="constant"
                            value="Current_thread" />
        </location>
        <location id="CurrentThreadName">
            <stateAttribute type="location"
                            value="CurrentCPU" />
            <stateAttribute type="constant"
                            value="Current_thread_name" />
        </location>
        <mappingGroup id="lock/unlock">
            <entry>
                <stateValue type="long"
                            value="128" />
                <stateValue type="string"
                            value="WAIT" />
            </entry>
            <entry>
                <stateValue type="long"
                            value="137" />
                <stateValue type="string"
                            value="WAIT_BITSET" />
            </entry>
            <entry>
                <stateValue type="long"
                            value="134" />
                <stateValue type="string"
                            value="LOCK_PI" />
            </entry>
            <entry>
                <stateValue type="long"
                            value="136" />
                <stateValue type="string"
                            value="TRYLOCK_PI" />
            </entry>
            <entry>
                <stateValue type="long"
                            value="129" />
                <stateValue type="string"
                            value="WAKE" />
            </entry>
            <entry>
                <stateValue type="long"
                            value="138" />
                <stateValue type="string"
                            value="WAKE_BITSET" />
            </entry>
            <entry>
                <stateValue type="long"
                            value="135" />
                <stateValue type="string"
                            value="UNLOCK_PI" />
            </entry>
            <entry>
                <stateValue type="long"
                            value="133" />
                <stateValue type="string"
                            value="WAKE_OP" />
            </entry>
        </mappingGroup>
        <patternHandler>
            <test id="futex_condition">
                <if>
                    <condition>
                        <stateValue type="string"
                                    stack="peek">
                            <stateAttribute type="constant"
                                            value="stack" />
                            <stateAttribute type="query">
                                <stateAttribute type="location"
                                                value="CurrentThread" />
                            </stateAttribute>
                        </stateValue>
                        <stateValue type="string"
                                    value="sys_futex" />
                    </condition>
                </if>
            </test>
            <test id="unlock_op">
                <if>
                    <or>
                        <condition>
                            <field name="op" />
                            <stateValue type="long"
                                        value="129" />
                        </condition>
                        <condition>
                            <field name="op" />
                            <stateValue type="long"
                                        value="138" />
                        </condition>
                        <condition>
                            <field name="op" />
                            <stateValue type="long"
                                        value="135" />
                        </condition>
                        <condition>
                            <field name="op" />
                            <stateValue type="long"
                                        value="133" />
                        </condition>
                    </or>
                </if>
            </test>
            <test id="lock_op">
                <if>
                    <or>
                        <condition>
                            <field name="op" />
                            <stateValue type="long"
                                        value="128" />
                        </condition>
                        <condition>
                            <field name="op" />
                            <stateValue type="long"
                                        value="137" />
                        </condition>
                        <condition>
                            <field name="op" />
                            <stateValue type="long"
                                        value="134" />
                        </condition>
                        <condition>
                            <field name="op" />
                            <stateValue type="long"
                                        value="136" />
                        </condition>
                    </or>
                </if>
            </test>
            <test id="tid_condition">
                <if>
                    <condition>
                        <stateValue type="query">
                            <stateAttribute type="constant"
                                            value="#CurrentScenario" />
                            <stateAttribute type="constant"
                                            value="thread" />
                        </stateValue>
                        <stateValue type="query">
                            <stateAttribute type="location"
                                            value="CurrentThread" />
                        </stateValue>
                    </condition>
                </if>
            </test>
            <test id="isTidValid">
                <if>
                    <not>
                        <condition>
                            <stateAttribute type="location"
                                            value="CurrentThread" />
                            <stateValue type="null" />
                        </condition>
                    </not>
                </if>
            </test>
            <!-- FUTEX FSM ACTIONS -->
            <action id="set_operation">
                <stateChange>
                    <stateAttribute type="constant"
                                    value="#CurrentScenario" />
                    <stateAttribute type="constant"
                                    value="op" />
                    <stateValue type="eventField"
                                value="op" />
                </stateChange>
            </action>
            <action id="waiter_in">
                <stateChange>
                    <stateAttribute type="constant"
                                    value="lock" />
                    <stateAttribute type="query">
                        <stateAttribute type="constant"
                                        value="#CurrentScenario" />
                        <stateAttribute type="constant"
                                        value="uaddr" />
                    </stateAttribute>
                    <stateAttribute type="query">
                        <stateAttribute type="constant"
                                        value="#CurrentScenario" />
                        <stateAttribute type="constant"
                                        value="thread" />
                    </stateAttribute>
                    <stateValue type="int"
                                value="1" />
                </stateChange>
            </action>
            <action id="waiter_out">
                <stateChange>
                    <stateAttribute type="constant"
                                    value="lock" />
                    <stateAttribute type="query">
                        <stateAttribute type="constant"
                                        value="#CurrentScenario" />
                        <stateAttribute type="constant"
                                        value="uaddr" />
                    </stateAttribute>
                    <stateAttribute type="query">
                        <stateAttribute type="constant"
                                        value="#CurrentScenario" />
                        <stateAttribute type="constant"
                                        value="thread" />
                    </stateAttribute>
                    <stateValue type="null" />
                </stateChange>
            </action>
            <action id="create_futex_segment">
                <segment>
                    <segType>
                        <segName>
                            <stateValue type="query"
                                        mappingGroup="lock/unlock">
                                <stateAttribute type="constant"
                                                value="#CurrentScenario" />
                                <stateAttribute type="constant"
                                                value="op" />
                            </stateValue>
                        </segName>
                    </segType>
                    <segContent>
                        <segField name="uaddr"
                                  type="string">
                            <stateValue type="query">
                                <stateAttribute type="constant"
                                                value="#CurrentScenario" />
                                <stateAttribute type="constant"
                                                value="uaddr" />
                            </stateValue>
                        </segField>
                        <segField name="name"
                                  type="string">
                            <stateValue type="query">
                                <stateAttribute type="constant"
                                                value="#CurrentScenario" />
                                <stateAttribute type="constant"
                                                value="thread_name" />
                            </stateValue>
                        </segField>
                        <segField name="thread"
                                  type="string">
                            <stateValue type="query">
                                <stateAttribute type="constant"
                                                value="#CurrentScenario" />
                                <stateAttribute type="constant"
                                                value="thread" />
                            </stateValue>
                        </segField>
                    </segContent>
                </segment>
            </action>
            <action id="saveContext">
                <stateChange>
                    <stateAttribute type="constant"
                                    value="#CurrentScenario" />
                    <stateAttribute type="constant"
                                    value="cpu" />
                    <stateValue type="eventField"
                                value="cpu" />
                </stateChange>
                <stateChange>
                    <stateAttribute type="constant"
                                    value="#CurrentScenario" />
                    <stateAttribute type="constant"
                                    value="uaddr" />
                    <stateValue type="eventField"
                                value="uaddr" />
                </stateChange>
                <stateChange>
                    <stateAttribute type="constant"
                                    value="#CurrentScenario" />
                    <stateAttribute type="constant"
                                    value="thread" />
                    <stateValue type="query">
                        <stateAttribute type="location"
                                        value="CurrentThread" />
                    </stateValue>
                </stateChange>
                <stateChange>
                    <stateAttribute type="constant"
                                    value="#CurrentScenario" />
                    <stateAttribute type="constant"
                                    value="thread_name" />
                    <stateValue type="query">
                        <stateAttribute type="location"
                                        value="CurrentThreadName" />
                    </stateValue>
                </stateChange>
            </action>
            <!-- SYSCALL FSM ACTIONS -->
            <action id="push_syscall">
                <stateChange>
                    <stateAttribute type="constant"
                                    value="stack" />
                    <stateAttribute type="query">
                        <stateAttribute type="location"
                                        value="CurrentCPU" />
                        <stateAttribute type="constant"
                                        value="Current_thread" />
                    </stateAttribute>
                    <stateValue stack="push"
                                type="eventName" />
                </stateChange>
            </action>
            <action id="pop_syscall">
                <stateChange>
                    <stateAttribute type="constant"
                                    value="stack" />
                    <stateAttribute type="query">
                        <stateAttribute type="location"
                                        value="CurrentCPU" />
                        <stateAttribute type="constant"
                                        value="Current_thread" />
                    </stateAttribute>
                    <stateValue stack="pop"
                                type="string" />
                </stateChange>
            </action>
            <fsm id="futex_lock_2_4">
                <precondition event="*sys*"
                              cond="isTidValid" />
                <initialState>
                    <transition event="sys_futex"
                                cond="isTidValid:lock_op"
                                target="syscall_entry_x"
                                action="saveContext:set_operation:waiter_in" />
                </initialState>
                <state id="syscall_entry_x">
                    <transition event="exit_syscall"
                                cond="futex_condition:tid_condition"
                                target="syscall_exit_x"
                                action="waiter_out:create_futex_segment" />
                </state>
                <final id="syscall_exit_x" />
            </fsm>
            <fsm id="futex_unlock_2_4">
                <precondition event="*sys*"
                              cond="isTidValid" />
                <initialState>
                    <transition event="sys_futex"
                                cond="isTidValid:unlock_op"
                                target="syscall_entry_x"
                                action="saveContext:set_operation" />
                </initialState>
                <state id="syscall_entry_x">
                    <transition event="exit_syscall"
                                cond="futex_condition:tid_condition"
                                target="syscall_exit_x"
                                action="create_futex_segment" />
                </state>
                <final id="syscall_exit_x" />
            </fsm>
            <fsm id="stack"
                 multiple="false">
                <precondition event="sys_*" />
                <precondition event="exit_syscall" />
                <precondition cond="isTidValid" />
                <state id="foo">
                    <transition event="sys_*"
                                target="foo"
                                action="push_syscall" />
                    <transition event="exit_syscall"
                                target="foo"
                                action="pop_syscall" />
                </state>
            </fsm>
            <fsm id="futex_lock_2_7">
                <precondition event="syscall_*_futex"
                              cond="isTidValid" />
                <initialState>
                    <transition event="syscall_entry_futex"
                                cond="isTidValid:lock_op"
                                target="syscall_entry_x"
                                action="saveContext:set_operation:waiter_in" />
                </initialState>
                <state id="syscall_entry_x">
                    <transition event="syscall_exit_futex"
                                cond="tid_condition"
                                target="syscall_exit_x"
                                action="waiter_out:create_futex_segment" />
                </state>
                <final id="syscall_exit_x" />
            </fsm>
            <fsm id="futex_unlock_2_7">
                <precondition event="syscall_*_futex"
                              cond="isTidValid" />
                <initialState>
                    <transition event="syscall_entry_futex"
                                cond="isTidValid:unlock_op"
                                target="syscall_entry_x"
                                action="saveContext:set_operation" />
                </initialState>
                <state id="syscall_entry_x">
                    <transition event="syscall_exit_futex"
                                cond="tid_condition"
                                target="syscall_exit_x"
                                action="create_futex_segment" />
                </state>
                <final id="syscall_exit_x" />
            </fsm>
            <!-- SCHED_SWITCH -->
            <action id="update_current_thread">
                <stateChange>
                    <stateAttribute type="location"
                                    value="CurrentThread" />
                    <stateValue type="eventField"
                                value="next_tid" />
                </stateChange>
            </action>
            <action id="update_current_thread_name">
                <stateChange>
                    <stateAttribute type="location"
                                    value="CurrentThreadName" />
                    <stateValue type="eventField"
                                value="next_comm" />
                </stateChange>
            </action>
            <fsm id="sched_switch"
                 multiple="false">
                <precondition event="sched_switch" />
                <state id="sched_switch">
                    <transition target="sched_switch"
                                action="update_current_thread:update_current_thread_name" />
                </state>
            </fsm>
        </patternHandler>
    </pattern>
</tmfxml>''',
    "Track and display KVM exit reasons, showing the counts of each exit_reason over time in a delta format.":'''<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <xyView id="kernel.kvm.exit.xychart">
        <head>
            <analysis id="kernel.kvm.exit.sp" />
            <label value="Exit reasons" />
        </head>
        <entry path="Reasons/*"
               displayType="delta">
            <display type="self" />
        </entry>
    </xyView>
    <stateProvider id="kernel.kvm.exit.sp"
                   version="1">
        <head>
            <traceType id="org.eclipse.linuxtools.lttng2.kernel.tracetype" />
            <label value="KVM exit reasons" />
        </head>
        <!-- case 1 : exit_syscall : Fields: int64 ret -->
        <eventHandler eventName="kvm_exit">
            <stateChange>
                <stateAttribute type="constant"
                                value="Reasons" />
                <stateAttribute type="eventField"
                                value="exit_reason" />
                <stateValue type="int"
                            value="1"
                            increment="true" />
            </stateChange>
        </eventHandler>
    </stateProvider>
</tmfxml>''',
    "Monitor worker states by workerno for events: start (WORKING), wait (WAIT), and awake (IDLE).":'''<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <stateProvider id="test.element.placement"
                   version="1">
        <location id="CurrentWorker">
            <stateAttribute type="constant"
                            value="Worker" />
            <stateAttribute type="eventField"
                            value="workerno" />
        </location>
        <!-- StateValues -->
        <definedValue name="WORKING"
                      value="3" />
        <eventHandler eventName="start">
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentWorker" />
                <stateValue type="int"
                            value="$WORKING" />
            </stateChange>
        </eventHandler>
        <definedValue name="WAIT"
                      value="4" />
        <eventHandler eventName="wait">
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentWorker" />
                <stateValue type="int"
                            value="$WAIT" />
            </stateChange>
        </eventHandler>
        <definedValue name="IDLE"
                      value="5" />
        <eventHandler eventName="awake">
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentWorker" />
                <stateValue type="int"
                            value="$IDLE" />
            </stateChange>
        </eventHandler>
    </stateProvider>
</tmfxml>''',
    "Increment state value by 1 for any event name, used for tracking statistics.":'''<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <stateProvider id="test.xml.attributes"
                   version="1">
        <!-- Test a increment of one on an event name, like for statistics -->
        <eventHandler eventName="*">
            <stateChange>
                <stateAttribute type="eventName" />
                <stateValue type="int"
                            value="1"
                            increment="true" />
            </stateChange>
        </eventHandler>
    </stateProvider>
</tmfxml>''',
     "Analyze call stack for threads, tracking function entry and exit using tid and op fields.":'''<?xml version="1.0" encoding="UTF-8"?>
<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <callstack id="callstack.analysis">
        <callstackGroup>
            <level path="threads/*" />
        </callstackGroup>
        <pattern version="0"
                 id="callstack.pattern">
            <head>
                <traceType id="org.eclipse.linuxtools.tmf.core.tests.xmlstub" />
                <label value="Test XML callstack" />
            </head>
            <patternHandler>
                <action id="functionEntry">
                    <stateChange>
                        <stateAttribute type="constant"
                                        value="threads" />
                        <stateAttribute type="eventField"
                                        value="tid" />
                        <stateAttribute type="constant"
                                        value="CallStack" />
                        <stateValue type="eventField"
                                    value="op"
                                    stack="push" />
                    </stateChange>
                </action>
                <action id="functionExit">
                    <stateChange>
                        <stateAttribute type="constant"
                                        value="threads" />
                        <stateAttribute type="eventField"
                                        value="tid" />
                        <stateAttribute type="constant"
                                        value="CallStack" />
                        <stateValue type="eventField"
                                    value="op"
                                    stack="pop" />
                    </stateChange>
                </action>
                <fsm id="callstack"
                     multiple="false"
                     initial="oneState">
                    <state id="oneState">
                        <transition event="entry"
                                    target="oneState"
                                    action="functionEntry" />
                        <transition event="exit"
                                    target="oneState"
                                    action="functionExit" />
                    </state>
                </fsm>
            </patternHandler>
        </pattern>
    </callstack>
    <timeGraphView id="callstack.pattern.tgview">
        <head>
            <analysis id="callstack.analysis" />
            <label value="XML Callstack SS view" />
        </head>
        <!-- StateValues -->
        <!-- Control Flow View -->
        <entry path="threads/*">
            <display type="self" />
            <entry path="callstack/*">
                <display type="self" />
            </entry>
        </entry>
    </timeGraphView>
</tmfxml>''',
    "Test condition operators with event 'sched_switch' to track process status changes using prev_tid and next_tid fields.":'''<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <stateProvider id="kernel.linux.sp"
                   version="1">
        <head>
            <traceType id="org.eclipse.linuxtools.lttng2.kernel.tracetype" />
            <label value="Test Condition Operators" />
        </head>
        <!-- StateValues -->
        <definedValue name="PROCESS_STATUS_UNKNOWN"
                      value="0" />
        <definedValue name="PROCESS_STATUS_WAIT_BLOCKED"
                      value="1" />
        <definedValue name="PROCESS_STATUS_RUN_USERMODE"
                      value="2" />
        <definedValue name="PROCESS_STATUS_RUN_SYSCALL"
                      value="3" />
        <definedValue name="PROCESS_STATUS_INTERRUPTED"
                      value="5000" />
        <definedValue name="PROCESS_STATUS_WAIT_FOR_CPU"
                      value="10" />
        <location id="CurrentThread">
            <stateAttribute type="constant"
                            value="Threads" />
            <stateAttribute type="eventField"
                            value="next_tid" />
        </location>
        <eventHandler eventName="sched_switch">
            <stateChange>
                <if>
                    <condition operator="ne">
                        <!-- operator can also be "eq", "ge", "gt", "le", "lt" -->
                        <field name="prev_state" />
                        <stateValue type="long"
                                    value="0" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="constant"
                                    value="Threads" />
                    <stateAttribute type="eventField"
                                    value="prev_tid" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$PROCESS_STATUS_WAIT_BLOCKED" />
                </then>
                <else>
                    <stateAttribute type="constant"
                                    value="Threads" />
                    <stateAttribute type="eventField"
                                    value="prev_tid" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$PROCESS_STATUS_WAIT_FOR_CPU" />
                </else>
            </stateChange>
            <stateChange>
                <if>
                    <condition operator="gt">
                        <field name="next_tid" />
                        <stateValue type="long"
                                    value="0" />
                    </condition>
                </if>
                <then>
                    <if>
                        <condition>
                            <!-- when the operation attribute is not set it is considered as "eq" (equal) -->
                            <stateAttribute type="location"
                                            value="newCurrentThread" />
                            <stateAttribute type="constant"
                                            value="System_call" />
                            <stateValue type="null" />
                        </condition>
                    </if>
                    <then>
                        <stateAttribute type="location"
                                        value="CurrentCPU" />
                        <stateAttribute type="constant"
                                        value="Status" />
                        <stateValue type="int"
                                    value="$CPU_STATUS_RUN_USERMODE" />
                    </then>
                    <else>
                        <stateAttribute type="location"
                                        value="CurrentCPU" />
                        <stateAttribute type="constant"
                                        value="Status" />
                        <stateValue type="int"
                                    value="$CPU_STATUS_RUN_SYSCALL" />
                    </else>
                </then>
            </stateChange>
            <stateChange>
                <if>
                    <condition>
                        <!-- when the operation attribute is not set it is considered as "eq" (equal) -->
                        <stateAttribute type="location"
                                        value="CurrentThread" />
                        <stateAttribute type="constant"
                                        value="System_call" />
                        <stateValue type="null" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="location"
                                    value="CurrentThread" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$PROCESS_STATUS_RUN_USERMODE" />
                </then>
                <else>
                    <stateAttribute type="location"
                                    value="CurrentThread" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$PROCESS_STATUS_RUN_SYSCALL" />
                </else>
            </stateChange>
        </eventHandler>
        <eventHandler eventName="irq_handler_exit">
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentIRQ" />
                <stateValue type="null" />
            </stateChange>
            <stateChange>
                <if>
                    <condition operator="eq">
                        <stateAttribute type="location"
                                        value="CurrentThread" />
                        <stateAttribute type="constant"
                                        value="System_call" />
                        <stateValue type="null" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="location"
                                    value="CurrentThread" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$PROCESS_STATUS_RUN_USERMODE" />
                </then>
                <else>
                    <stateAttribute type="location"
                                    value="CurrentThread" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$PROCESS_STATUS_RUN_SYSCALL" />
                </else>
            </stateChange>
        </eventHandler>
    </stateProvider>
</tmfxml>''',
    "Evaluate conditions using event handlers for 'test' and 'test1' events, with attributes like testField, checkpoint, and conditions like and_three_operands and not_operand.":'''<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <stateProvider id="test.xml.conditions"
                   version="1">
        <eventHandler eventName="test">
            <stateChange>
                <if>
                    <condition>
                        <field name="testField" />
                        <stateValue type="long"
                                    value="10" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="eventName" />
                    <stateValue type="long"
                                value="1" />
                </then>
                <else>
                    <stateAttribute type="eventName" />
                    <stateValue type="long"
                                value="0" />
                </else>
            </stateChange>
        </eventHandler>
        <eventHandler eventName="test1">
            <stateChange>
                <if>
                    <condition>
                        <field name="testField" />
                        <stateValue type="long"
                                    value="200" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="eventName" />
                    <stateValue type="long"
                                value="1" />
                </then>
                <else>
                    <stateAttribute type="eventName" />
                    <stateValue type="long"
                                value="0" />
                </else>
            </stateChange>
        </eventHandler>
        <eventHandler eventName="*">
            <stateChange>
                <if>
                    <condition>
                        <stateValue type="query">
                            <stateAttribute type="constant"
                                            value="test" />
                        </stateValue>
                        <stateValue type="query">
                            <stateAttribute type="constant"
                                            value="test1" />
                        </stateValue>
                    </condition>
                </if>
                <then>
                    <stateAttribute type="constant"
                                    value="checkpoint" />
                    <stateValue type="long"
                                value="1" />
                </then>
                <else>
                    <stateAttribute type="constant"
                                    value="checkpoint" />
                    <stateValue type="long"
                                value="0" />
                </else>
            </stateChange>
        </eventHandler>
        <eventHandler eventName="*">
            <stateChange>
                <if>
                    <and>
                        <condition>
                            <stateAttribute type="constant"
                                            value="test" />
                            <stateValue type="long"
                                        value="0" />
                        </condition>
                        <condition>
                            <stateAttribute type="constant"
                                            value="test1" />
                            <stateValue type="long"
                                        value="0" />
                        </condition>
                        <condition>
                            <stateAttribute type="constant"
                                            value="checkpoint" />
                            <stateValue type="long"
                                        value="1" />
                        </condition>
                    </and>
                </if>
                <then>
                    <stateAttribute type="constant"
                                    value="and_three_operands" />
                    <stateValue type="long"
                                value="0" />
                </then>
                <else>
                    <stateAttribute type="constant"
                                    value="and_three_operands" />
                    <stateValue type="long"
                                value="1" />
                </else>
            </stateChange>
        </eventHandler>
        <eventHandler eventName="*">
            <stateChange>
                <if>
                    <not>
                        <condition>
                            <stateAttribute type="constant"
                                            value="and_three_operands" />
                            <stateValue type="long"
                                        value="1" />
                        </condition>
                    </not>
                </if>
                <then>
                    <stateAttribute type="constant"
                                    value="not_operand" />
                    <stateValue type="long"
                                value="1" />
                </then>
                <else>
                    <stateAttribute type="constant"
                                    value="not_operand" />
                    <stateValue type="long"
                                value="0" />
                </else>
            </stateChange>
        </eventHandler>
    </stateProvider>
</tmfxml>''',
    "Analyze syscalls with patternHandler, using stateChange actions to increment counters for consuming and non-consuming events, and creating segments with mappings.":'''<?xml version="1.0" encoding="UTF-8"?>
<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <pattern version="0"
             id="syscall.analysis">
        <mappingGroup id="group">
            <entry>
                <stateValue type="int"
                            value="1" />
                <stateValue type="string"
                            value="open" />
            </entry>
        </mappingGroup>
        <patternHandler>
            <action id="increment_counter_consuming">
                <stateChange>
                    <stateAttribute type="constant"
                                    value="consuming" />
                    <stateValue increment="true"
                                type="long"
                                value="1" />
                </stateChange>
            </action>
            <fsm id="consuming">
                <state id="start">
                    <transition event="entry"
                                target="exit_state" />
                </state>
                <state id="exit_state">
                    <transition event="exit"
                                target="end"
                                action="increment_counter_consuming" />
                </state>
                <final id="end" />
            </fsm>
            <action id="increment_counter_non_consuming">
                <stateChange>
                    <stateAttribute type="constant"
                                    value="non_consuming" />
                    <stateValue increment="true"
                                type="long"
                                value="1" />
                </stateChange>
            </action>
            <fsm id="non_consuming"
                 consuming="false">
                <state id="start">
                    <transition event="entry"
                                target="exit_state" />
                </state>
                <state id="exit_state">
                    <transition event="exit"
                                target="end"
                                action="increment_counter_non_consuming" />
                </state>
                <final id="end" />
            </fsm>
            <action id="segment_create">
                <segment>
                    <segType>
                        <segName>
                            <stateValue mappingGroup="group"
                                        type="int"
                                        value="1" />
                        </segName>
                    </segType>
                </segment>
            </action>
            <fsm id="mapping"
                 multiple="false">
                <state id="start">
                    <transition event="entry"
                                target="end"
                                action="segment_create" />
                </state>
                <final id="end" />
            </fsm>
        </patternHandler>
    </pattern>
</tmfxml>''',
    "Visualize the XML simple pattern with time graph views and XY charts, analyzing CPU entries with display type and delta.":'''<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <timeGraphView id="xml.core.tests.simple.pattern.timegraph">
        <head>
            <analysis id="xml.core.tests.simple.pattern" />
            <label value="XML Simple Time Graph" />
        </head>
        <!-- Control Flow View -->
        <entry path="CPU">
            <display type="self" />
            <entry path="*">
                <display type="self" />
            </entry>
        </entry>
    </timeGraphView>
    <timeGraphView id="xml.core.tests.simple.pattern.timegraph2">
        <head>
            <analysis id="xml.core.tests.simple.pattern" />
            <label value="XML Simple Time Graph 2" />
        </head>
        <!-- Control Flow View -->
        <entry path="CPU">
            <entry path="*">
                <display type="self" />
            </entry>
        </entry>
    </timeGraphView>
    <xyView id="xml.core.tests.simple.pattern.xy">
        <head>
            <analysis id="xml.core.tests.simple.pattern" />
            <label value="XML Simple XY chart" />
        </head>
        <entry path="CPU/*">
            <display type="self" />
        </entry>
    </xyView>
    <xyView id="xml.core.tests.simple.pattern.xy.delta">
        <head>
            <analysis id="xml.core.tests.simple.pattern" />
            <label value="XML Simple XY chart with delta" />
        </head>
        <entry path="CPU/*"
               displayType="delta">
            <display type="self" />
        </entry>
    </xyView>
</tmfxml>''',
    "For the event 'x', store the value of 'testField' as a double type in the XML state provider 'test.xml.doubles'.":'''<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <stateProvider id="test.xml.doubles"
                   version="1">
        <eventHandler eventName="x">
            <stateChange>
                <stateAttribute type="constant"
                                value="testField" />
                <stateValue type="eventField"
                            forcedType="double"
                            value="testField" />
            </stateChange>
        </eventHandler>
    </stateProvider>
</tmfxml>''',
    "For the experiment analysis 'test.xml.experiment.stateprovider', create a time graph view showing updates for each CPU. Define 'Good' and 'Bad' states with specific colors.":'''<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <timeGraphView id="test.xml.experiment.timegraph">
        <head>
            <analysis id="test.xml.experiment.stateprovider" />
            <label value="Test XML Experiment view" />
        </head>
        <!-- Test string value for colors for this analysis -->
        <definedValue name="Good"
                      value="GOOD"
                      color="#118811" />
        <definedValue name="Bad"
                      value="BAD"
                      color="#DDDD00" />
        <entry path="update/*">
            <display type="self" />
        </entry>
    </timeGraphView>
    <stateProvider id="test.xml.experiment.stateprovider"
                   version="1">
        <head>
            <traceType id="org.eclipse.linuxtools.tmf.core.experiment.generic" />
            <label value="Xml Analysis for experiments only" />
        </head>
        <mappingGroup id="operation">
            <entry>
                <stateValue type="string"
                            value="read only" />
                <stateValue type="string"
                            value="op1" />
            </entry>
        </mappingGroup>
        <!-- Test to see that state values are updated or modified depending on the requested state change -->
        <eventHandler eventName="entry">
            <stateChange>
                <stateAttribute type="constant"
                                value="update" />
                <stateAttribute type="eventField"
                                value="cpu" />
                <stateValue type="string"
                            value="UNKNOWN" />
            </stateChange>
        </eventHandler>
        <eventHandler eventName="exit">
            <stateChange>
                <stateAttribute type="constant"
                                value="update" />
                <stateAttribute type="eventField"
                                value="cpu" />
                <stateValue type="eventField"
                            value="curState"
                            update="true" />
            </stateChange>
        </eventHandler>
    </stateProvider>
</tmfxml>''',
    "Analyze the 'test.analysis.1' pattern to check if 'curState' equals 'GOOD' and increment counters for fsm1, fsm2, and fsm3 based on transitions.":'''<?xml version="1.0" encoding="UTF-8"?>
<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <pattern version="0"
             id="test.analysis.1">
        <head>
            <traceType id="org.eclipse.linuxtools.tmf.core.tests.xmlstub" />
            <label value="XML test analysis 1" />
        </head>
        <patternHandler>
            <!-- This condition check if the current running thread PID is 496 -->
            <test id="curState">
                <if>
                    <condition>
                        <field name="curState" />
                        <stateValue type="string"
                                    value="GOOD" />
                    </condition>
                </if>
            </test>
            <action id="increment_fsm1_counter">
                <stateChange>
                    <stateAttribute type="constant"
                                    value="fsm1" />
                    <stateValue type="long"
                                value="1"
                                increment="true" />
                </stateChange>
            </action>
            <action id="increment_fsm2_counter">
                <stateChange>
                    <stateAttribute type="constant"
                                    value="fsm2" />
                    <stateValue type="long"
                                value="1"
                                increment="true" />
                </stateChange>
            </action>
            <action id="increment_fsm3_counter">
                <stateChange>
                    <stateAttribute type="constant"
                                    value="fsm3" />
                    <stateValue type="long"
                                value="1"
                                increment="true" />
                </stateChange>
            </action>
            <fsm id="fsm1">
                <initial>
                    <transition cond="curState"
                                target="state1" />
                </initial>
                <state id="state1">
                    <transition event="exit"
                                target="end"
                                action="increment_fsm1_counter" />
                </state>
                <final id="end" />
            </fsm>
            <fsm id="fsm2">
                <initialState>
                    <transition event="exit"
                                target="end"
                                action="increment_fsm2_counter" />
                </initialState>
                <final id="end" />
            </fsm>
            <fsm id="fsm3">
                <initialState>
                    <transition event="exit"
                                cond="curState"
                                target="end"
                                action="increment_fsm3_counter" />
                </initialState>
                <final id="end" />
            </fsm>
        </patternHandler>
    </pattern>
</tmfxml>''',
    "Analyze the 'test.analysis.2' pattern, check if 'curState' equals 'BAD', increment counters 'count_new' and 'precond', and generate segments 'OLD' and 'NEW'.":'''<?xml version="1.0" encoding="UTF-8"?>
<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <pattern version="0"
             id="test.analysis.2">
        <head>
            <traceType id="org.eclipse.linuxtools.tmf.core.tests.xmlstub" />
            <label value="XML test analysis 2" />
        </head>
        <patternHandler>
            <test id="curStateBad">
                <if>
                    <condition>
                        <field name="curState" />
                        <stateValue type="string"
                                    value="BAD" />
                    </condition>
                </if>
            </test>
            <action id="increment_counter_new">
                <stateChange>
                    <stateAttribute type="constant"
                                    value="count_new" />
                    <stateValue type="int"
                                value="1"
                                increment="true" />
                </stateChange>
            </action>
            <action id="increment_counter_precond">
                <stateChange>
                    <stateAttribute type="constant"
                                    value="precond" />
                    <stateValue type="int"
                                value="1"
                                increment="true" />
                </stateChange>
            </action>
            <action id="generate_old_segment">
                <segment>
                    <segType segName="OLD" />
                </segment>
            </action>
            <action id="generate_new_segment">
                <segment>
                    <segType segName="NEW" />
                </segment>
            </action>
            <fsm id="test"
                 initial="state_old"
                 multiple="false">
                <initial>
                    <transition target="state_old" />
                </initial>
                <initialState>
                    <transition target="state_new" />
                </initialState>
                <state id="state_old">
                    <transition target="end"
                                action="generate_old_segment" />
                </state>
                <state id="state_new">
                    <transition target="end"
                                action="generate_new_segment" />
                </state>
                <final id="end" />
            </fsm>
            <fsm id="test1"
                 multiple="false">
                <!-- There is only one such event, so it should pass the initial state, but go no further -->
                <precondition event="exit"
                              cond="curStateBad" />
                <initialState>
                    <transition target="state_new"
                                action="increment_counter_new" />
                </initialState>
                <state id="state_new">
                    <transition target="state_2"
                                action="increment_counter_precond" />
                </state>
                <state id="state_2">
                    <transition target="end"
                                action="increment_counter_precond" />
                </state>
                <final id="end" />
            </fsm>
        </patternHandler>
    </pattern>
</tmfxml>''',
    "Analyze the 'xml test pattern segment', generate segments 'test1' and 'test2' with fields 'field1', 'field2', 'field3', and toggle states on 'test' and 'test1' events.":'''<?xml version="1.0" encoding="UTF-8"?>
<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <pattern version="0"
             id="xml test pattern segment">
        <head>
            <traceType id="org.eclipse.linuxtools.lttng2.kernel.tracetype" />
            <label value="xml test pattern segment" />
        </head>
        <!-- the pattern handler specifies the FSM that will be instanciated at the beginning of the analysis -->
        <patternHandler initial="test">
            <!-- CONDITIONS -->
            <!-- ACTIONS -->
            <!-- Generate two segments -->
            <action id="pattern segment test 1">
                <!-- Generate a pattern segment with the name 'test1' -->
                <segment>
                    <segType segName="test1" />
                </segment>
            </action>
            <action id="pattern segment test 2">
                <!-- Generate a pattern segment with the name 'test2' and with three fields 'field1', 'field2' and 'field3' -->
                <segment>
                    <segType segName="test2" />
                    <segContent>
                        <segField name="field1"
                                  type="long">
                            <stateValue type="eventField"
                                        value="testField" />
                        </segField>
                        <segField name="field2"
                                  type="string"
                                  value="test" />
                        <segField name="field3"
                                  type="int"
                                  value="1" />
                    </segContent>
                </segment>
            </action>
            <!-- FSMs -->
            <!-- test fsm
		Declare a test FSM that will go back and forth between 2 states -->
            <fsm id="test"
                 multiple="true"
                 initial="state1">
                <state id="state1">
                    <transition event="test"
                                target="state2"
                                action="pattern segment test 1" />
                </state>
                <state id="state2">
                    <transition event="test1"
                                target="state1"
                                action="pattern segment test 2" />
                </state>
            </fsm>
        </patternHandler>
    </pattern>
</tmfxml>''',
    "Create a segment named 'seg1' with start time from 'timestamp' and end time from 'testField', and transition from 'start' to 'end' state on any event.":'''<?xml version="1.0" encoding="UTF-8"?>
<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <pattern version="0"
             id="test.seg.duration">
        <head>
            <label value="analysis name" />
        </head>
        <patternHandler>
            <action id="segment_create">
                <segment>
                    <segType>
                        <segName>
                            <stateValue type="string"
                                        value="seg1" />
                        </segName>
                    </segType>
                    <segTime>
                        <begin type="eventField"
                               value="timestamp" />
                        <end type="eventField"
                             value="testField" />
                    </segTime>
                </segment>
            </action>
            <fsm id="test"
                 multiple="true">
                <state id="start">
                    <transition event="*"
                                target="end"
                                action="segment_create" />
                </state>
                <final id="end" />
            </fsm>
        </patternHandler>
    </pattern>
</tmfxml>''',
    "Display the 'Test XML Attributes view' with updates and modifications on 'cpu', handling various state changes, future time calculations, and conditional operations on events like 'entry' and 'exit'.":'''<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <timeGraphView id="org.eclipse.linuxtools.tmf.analysis.xml.ui.views.statesystem">
        <head>
            <analysis id="test.xml.attributes" />
            <label value="Test XML Attributes view" />
        </head>
        <!-- Test string value for colors for this analysis -->
        <definedValue name="Good"
                      value="GOOD"
                      color="#118811" />
        <definedValue name="Bad"
                      value="BAD"
                      color="#DDDD00" />
        <entry path="update/*">
            <display type="self" />
        </entry>
    </timeGraphView>
    <stateProvider id="test.xml.attributes"
                   version="1">
        <head>
            <traceType id="org.eclipse.linuxtools.tmf.core.tests.xmlstub" />
            <label value="Xml State Values test" />
        </head>
        <mappingGroup id="operation">
            <entry>
                <stateValue type="string"
                            value="read only" />
                <stateValue type="string"
                            value="op1" />
            </entry>
        </mappingGroup>
        <!-- Test to see that state values are updated or modified depending on the requested state change -->
        <eventHandler eventName="entry">
            <stateChange>
                <stateAttribute type="constant"
                                value="update" />
                <stateAttribute type="eventField"
                                value="cpu" />
                <stateValue type="string"
                            value="UNKNOWN" />
            </stateChange>
            <stateChange>
                <stateAttribute type="constant"
                                value="modify" />
                <stateAttribute type="eventField"
                                value="cpu" />
                <stateValue type="string"
                            value="UNKNOWN" />
            </stateChange>
            <stateChange>
                <stateAttribute type="constant"
                                value="hostID" />
                <stateValue type="eventField"
                            value="hostID" />
            </stateChange>
            <stateChange>
                <stateAttribute type="constant"
                                value="stack" />
                <stateValue stack="push"
                            type="eventField"
                            value="timestamp" />
            </stateChange>
            <stateChange>
                <if>
                    <condition>
                        <field name="op" />
                        <stateValue mappingGroup="operation"
                                    type="string"
                                    value="read only" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="constant"
                                    value="mapped" />
                    <stateValue type="string"
                                value="TRUE" />
                </then>
                <else>
                    <stateAttribute type="constant"
                                    value="mapped" />
                    <stateValue type="string"
                                value="FALSE" />
                </else>
            </stateChange>
            <stateChange>
                <stateAttribute type="constant"
                                value="script" />
                <stateValue type="script"
                            value="op == 'op1' ? 'TRUE' : 'FALSE'"
                            scriptEngine="rhino">
                    <stateValue id="op"
                                type="eventField"
                                value="op" />
                </stateValue>
            </stateChange>
            <stateChange>
                <stateAttribute type="constant"
                                value="future" />
                <stateValue type="int"
                            value="100" />
            </stateChange>
            <stateChange>
                <stateAttribute type="constant"
                                value="future" />
                <stateValue type="int"
                            value="101" />
                <futureTime type="script"
                            value="ts + 2"
                            scriptEngine="rhino">
                    <stateValue id="ts"
                                type="eventField"
                                value="timestamp" />
                </futureTime>
            </stateChange>
            <stateChange>
                <stateAttribute type="constant"
                                value="futureStr" />
                <stateValue type="int"
                            value="100" />
            </stateChange>
            <stateChange>
                <stateAttribute type="constant"
                                value="futureStr" />
                <stateValue type="int"
                            value="101" />
                <futureTime type="script"
                            value="ts + 2"
                            scriptEngine="rhino"
                            forcedType="string">
                    <stateValue id="ts"
                                type="eventField"
                                value="timestamp" />
                </futureTime>
            </stateChange>
            <stateChange>
                <stateAttribute type="constant"
                                value="futureStack" />
                <stateAttribute type="eventField"
                                value="cpu" />
                <stateValue type="eventField"
                            value="op"
                            stack="push" />
                <futureTime type="script"
                            value="ts + 1"
                            scriptEngine="rhino">
                    <stateValue id="ts"
                                type="eventField"
                                value="timestamp" />
                </futureTime>
            </stateChange>
            <stateChange>
                <stateAttribute type="constant"
                                value="futureStack" />
                <stateAttribute type="eventField"
                                value="cpu" />
                <stateValue type="eventField"
                            value="op"
                            stack="pop" />
                <futureTime type="script"
                            value="ts + 6"
                            scriptEngine="rhino">
                    <stateValue id="ts"
                                type="eventField"
                                value="timestamp" />
                </futureTime>
            </stateChange>
        </eventHandler>
        <eventHandler eventName="exit">
            <stateChange>
                <stateAttribute type="constant"
                                value="update" />
                <stateAttribute type="eventField"
                                value="cpu" />
                <stateValue type="eventField"
                            value="curState"
                            update="true" />
            </stateChange>
            <stateChange>
                <stateAttribute type="constant"
                                value="update" />
                <stateAttribute type="eventField"
                                value="cpu" />
                <stateValue type="null" />
            </stateChange>
            <stateChange>
                <stateAttribute type="constant"
                                value="modify" />
                <stateAttribute type="eventField"
                                value="cpu" />
                <stateValue type="eventField"
                            value="curState" />
            </stateChange>
            <stateChange>
                <if>
                    <condition>
                        <stateValue type="long"
                                    stack="peek">
                            <stateAttribute type="constant"
                                            value="stack" />
                        </stateValue>
                        <stateValue type="long"
                                    value="5" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="constant"
                                    value="stack" />
                    <stateValue stack="pop"
                                type="null" />
                </then>
            </stateChange>
            <stateChange>
                <if>
                    <condition>
                        <field name="op" />
                        <stateValue type="string"
                                    value="read only" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="constant"
                                    value="mapped" />
                    <stateValue type="string"
                                value="TRUE" />
                </then>
                <else>
                    <stateAttribute type="constant"
                                    value="mapped" />
                    <stateValue type="string"
                                value="FALSE" />
                </else>
            </stateChange>
            <stateChange>
                <stateAttribute type="constant"
                                value="script" />
                <stateValue type="script"
                            value="op == 'op1' ? 'FALSE' : 'TRUE'"
                            scriptEngine="rhino">
                    <stateValue id="op"
                                type="eventField"
                                value="op" />
                </stateValue>
            </stateChange>
        </eventHandler>
    </stateProvider>
</tmfxml>''',
    "Test the state values in an FSM scenario. Handle events like 'entry', 'exit', and 'action', saving 'op' in an attribute pool and checking 'cpu' state in the process.":'''<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <!-- This file will test state values in the context of an fsm -->
    <pattern version="0"
             id="org.eclipse.tracecompass.xml.tests.statevaluescenarios">
        <patternHandler initial="test">
            <test id="cpu">
                <if>
                    <condition>
                        <stateValue type="query">
                            <stateAttribute type="constant"
                                            value="#CurrentScenario" />
                            <stateAttribute type="constant"
                                            value="cpu" />
                        </stateValue>
                        <stateValue type="eventField"
                                    value="cpu" />
                    </condition>
                </if>
            </test>
            <!-- ACTIONS -->
            <!-- Save a value in an attribute pool -->
            <action id="save_pool">
                <stateChange>
                    <stateAttribute type="constant"
                                    value="Operations" />
                    <stateAttribute type="pool" />
                    <stateValue type="eventField"
                                value="op" />
                </stateChange>
                <stateChange>
                    <stateAttribute type="constant"
                                    value="#CurrentScenario" />
                    <stateAttribute type="constant"
                                    value="cpu" />
                    <stateValue type="eventField"
                                value="cpu" />
                </stateChange>
            </action>
            <!-- A different action, to test that the attribute pool is shared in a same analysis -->
            <action id="save_pool2">
                <stateChange>
                    <stateAttribute type="constant"
                                    value="Operations" />
                    <stateAttribute type="pool" />
                    <stateValue type="eventField"
                                value="op" />
                </stateChange>
            </action>
            <!-- FSMs -->
            <!-- test fsm
			Declare a test FSM that that will generate two segments for each event received -->
            <fsm id="test"
                 initial="wait_entry">
                <state id="wait_entry">
                    <transition event="entry"
                                target="in_scenario"
                                action="save_pool" />
                </state>
                <state id="in_scenario">
                    <transition cond="cpu"
                                event="exit"
                                target="end" />
                    <transition cond="cpu"
                                event="action"
                                target="in_scenario"
                                action="save_pool2" />
                </state>
                <final id="end" />
            </fsm>
        </patternHandler>
    </pattern>
</tmfxml>''',
    "Analyze kernel Linux state system with events like 'exit_syscall', 'irq_handler_entry', and 'sched_switch', updating status of CPUs and threads accordingly.":'''<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <timeGraphView id="org.eclipse.linuxtools.tmf.analysis.xml.ui.views.statesystem">
        <head>
            <analysis id="kernel.linux.sp" />
            <label value="Xml Sample Kernel View" />
        </head>
        <!-- StateValues -->
        <definedValue name="PROCESS_STATUS_UNKNOWN"
                      value="0"
                      color="#EEEEEE" />
        <definedValue name="PROCESS_STATUS_WAIT_BLOCKED"
                      value="1"
                      color="#CCCCCC" />
        <definedValue name="PROCESS_STATUS_RUN_USERMODE"
                      value="2"
                      color="#118811" />
        <definedValue name="PROCESS_STATUS_RUN_SYSCALL"
                      value="3"
                      color="#0000EE" />
        <definedValue name="PROCESS_STATUS_INTERRUPTED"
                      value="4"
                      color="#DDDD00" />
        <definedValue name="PROCESS_STATUS_WAIT_FOR_CPU"
                      value="5"
                      color="#AA0000" />
        <!-- Control Flow View -->
        <entry path="CPUs/*">
            <display type="constant"
                     value="Status" />
            <parent type="constant"
                    value="PPID" />
            <name type="constant"
                  value="Exec_name" />
        </entry>
        <entry path="Threads">
            <display type="self" />
            <entry path="*">
                <display type="constant"
                         value="Status" />
                <parent type="constant"
                        value="PPID" />
                <name type="constant"
                      value="Exec_name" />
            </entry>
        </entry>
    </timeGraphView>
    <xyView id="org.eclipse.linuxtools.tmf.analysis.xml.core.tests.xy">
        <head>
            <analysis id="kernel.linux.sp" />
        </head>
        <entry path="CPUs/*">
            <display type="constant"
                     value="Status" />
            <name type="self" />
        </entry>
    </xyView>
    <stateProvider id="kernel.linux.sp"
                   version="1">
        <head>
            <traceType id="org.eclipse.linuxtools.lttng2.kernel.tracetype" />
            <label value="Xml kernel State System" />
        </head>
        <!-- StateValues -->
        <definedValue name="CPU_STATUS_IDLE"
                      value="0" />
        <definedValue name="CPU_STATUS_RUN_USERMODE"
                      value="1" />
        <definedValue name="CPU_STATUS_RUN_SYSCALL"
                      value="2" />
        <definedValue name="CPU_STATUS_IRQ"
                      value="3" />
        <definedValue name="CPU_STATUS_SOFTIRQ"
                      value="4" />
        <definedValue name="PROCESS_STATUS_UNKNOWN"
                      value="0" />
        <definedValue name="PROCESS_STATUS_WAIT_BLOCKED"
                      value="1" />
        <definedValue name="PROCESS_STATUS_RUN_USERMODE"
                      value="2" />
        <definedValue name="PROCESS_STATUS_RUN_SYSCALL"
                      value="3" />
        <definedValue name="PROCESS_STATUS_INTERRUPTED"
                      value="4" />
        <definedValue name="PROCESS_STATUS_WAIT_FOR_CPU"
                      value="5" />
        <definedValue name="SOFT_IRQ_RAISED"
                      value="-2" />
        <!-- Shortcut Variables -->
        <location id="CurrentThread">
            <stateAttribute type="constant"
                            value="Threads" />
            <stateAttribute type="query">
                <stateAttribute type="constant"
                                value="CPUs" />
                <stateAttribute type="eventField"
                                value="cpu" />
                <stateAttribute type="constant"
                                value="Current_thread" />
            </stateAttribute>
        </location>
        <location id="CurrentCPU">
            <stateAttribute type="constant"
                            value="CPUs" />
            <stateAttribute type="eventField"
                            value="cpu" />
        </location>
        <location id="CurrentIRQ">
            <stateAttribute type="constant"
                            value="Resources" />
            <stateAttribute type="constant"
                            value="IRQs" />
            <stateAttribute type="eventField"
                            value="irq" />
        </location>
        <location id="CurrentSoftIRQ">
            <stateAttribute type="constant"
                            value="Resources" />
            <stateAttribute type="constant"
                            value="Soft_IRQs" />
            <stateAttribute type="eventField"
                            value="vec" />
        </location>
        <location id="newCurrentThread">
            <stateAttribute type="constant"
                            value="Threads" />
            <stateAttribute type="eventField"
                            value="next_tid" />
        </location>
        <!-- case 1 : exit_syscall : Fields: int64 ret -->
        <eventHandler eventName="exit_syscall">
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentThread" />
                <stateAttribute type="constant"
                                value="System_call" />
                <stateValue type="null" />
            </stateChange>
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentThread" />
                <stateAttribute type="constant"
                                value="Status" />
                <stateValue type="int"
                            value="$PROCESS_STATUS_RUN_USERMODE" />
            </stateChange>
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentCPU" />
                <stateAttribute type="constant"
                                value="Status" />
                <stateValue type="int"
                            value="$CPU_STATUS_RUN_USERMODE" />
            </stateChange>
        </eventHandler>
        <!-- case 2 : irq_handler_entry : Fields: int32 irq, string name -->
        <eventHandler eventName="irq_handler_entry">
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentIRQ" />
                <stateValue type="eventField"
                            value="cpu" />
            </stateChange>
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentThread" />
                <stateAttribute type="constant"
                                value="Status" />
                <stateValue type="int"
                            value="$PROCESS_STATUS_INTERRUPTED" />
            </stateChange>
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentCPU" />
                <stateAttribute type="constant"
                                value="Status" />
                <stateValue type="int"
                            value="$CPU_STATUS_IRQ" />
            </stateChange>
        </eventHandler>
        <!-- case 3 : irq_handler_exit : Fields: int32 irq, int32 ret -->
        <eventHandler eventName="irq_handler_exit">
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentIRQ" />
                <stateValue type="null" />
            </stateChange>
            <stateChange>
                <if>
                    <condition>
                        <stateAttribute type="location"
                                        value="CurrentThread" />
                        <stateAttribute type="constant"
                                        value="System_call" />
                        <stateValue type="null" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="location"
                                    value="CurrentThread" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$PROCESS_STATUS_RUN_USERMODE" />
                </then>
                <else>
                    <stateAttribute type="location"
                                    value="CurrentThread" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$PROCESS_STATUS_RUN_SYSCALL" />
                </else>
            </stateChange>
            <stateChange>
                <if>
                    <condition>
                        <stateAttribute type="location"
                                        value="CurrentThread" />
                        <stateAttribute type="constant"
                                        value="System_call" />
                        <stateValue type="null" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="location"
                                    value="CurrentCPU" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$CPU_STATUS_RUN_USERMODE" />
                </then>
                <else>
                    <stateAttribute type="location"
                                    value="CurrentCPU" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$CPU_STATUS_RUN_SYSCALL" />
                </else>
            </stateChange>
            <stateChange>
                <if>
                    <condition>
                        <stateAttribute type="location"
                                        value="CurrentCPU" />
                        <stateAttribute type="constant"
                                        value="Current_thread" />
                        <stateValue type="null" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="location"
                                    value="CurrentCPU" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$CPU_STATUS_IDLE" />
                </then>
            </stateChange>
            <stateChange>
                <if>
                    <condition>
                        <stateAttribute type="location"
                                        value="CurrentCPU" />
                        <stateAttribute type="constant"
                                        value="Current_thread" />
                        <stateValue type="int"
                                    value="0" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="location"
                                    value="CurrentCPU" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$CPU_STATUS_IDLE" />
                </then>
            </stateChange>
        </eventHandler>
        <!-- case 4 : softirq_entry : Fields: int32 vec -->
        <eventHandler eventName="softirq_entry">
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentSoftIRQ" />
                <stateValue type="eventField"
                            value="cpu" />
            </stateChange>
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentThread" />
                <stateAttribute type="constant"
                                value="Status" />
                <stateValue type="int"
                            value="$PROCESS_STATUS_INTERRUPTED" />
            </stateChange>
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentCPU" />
                <stateAttribute type="constant"
                                value="Status" />
                <stateValue type="int"
                            value="$CPU_STATUS_SOFTIRQ" />
            </stateChange>
        </eventHandler>
        <!-- case 5 : softirq_exit : Fields: int32 vec -->
        <eventHandler eventName="softirq_exit">
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentSoftIRQ" />
                <stateValue type="null" />
            </stateChange>
            <stateChange>
                <if>
                    <condition>
                        <stateAttribute type="location"
                                        value="CurrentThread" />
                        <stateAttribute type="constant"
                                        value="System_call" />
                        <stateValue type="null" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="location"
                                    value="CurrentThread" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$PROCESS_STATUS_RUN_USERMODE" />
                </then>
                <else>
                    <stateAttribute type="location"
                                    value="CurrentThread" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$PROCESS_STATUS_RUN_SYSCALL" />
                </else>
            </stateChange>
            <stateChange>
                <if>
                    <condition>
                        <stateAttribute type="location"
                                        value="CurrentThread" />
                        <stateAttribute type="constant"
                                        value="System_call" />
                        <stateValue type="null" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="location"
                                    value="CurrentCPU" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$CPU_STATUS_RUN_USERMODE" />
                </then>
                <else>
                    <stateAttribute type="location"
                                    value="CurrentCPU" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$CPU_STATUS_RUN_SYSCALL" />
                </else>
            </stateChange>
            <stateChange>
                <if>
                    <condition>
                        <stateAttribute type="location"
                                        value="CurrentCPU" />
                        <stateAttribute type="constant"
                                        value="Current_thread" />
                        <stateValue type="null" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="location"
                                    value="CurrentCPU" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$CPU_STATUS_IDLE" />
                </then>
            </stateChange>
            <stateChange>
                <if>
                    <condition>
                        <stateAttribute type="location"
                                        value="CurrentCPU" />
                        <stateAttribute type="constant"
                                        value="Current_thread" />
                        <stateValue type="int"
                                    value="0" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="location"
                                    value="CurrentCPU" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$CPU_STATUS_IDLE" />
                </then>
            </stateChange>
        </eventHandler>
        <!-- case 6 : softirq_raise : Fields: int32 vec -->
        <eventHandler eventName="softirq_raise">
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentSoftIRQ" />
                <stateValue type="int"
                            value="$SOFT_IRQ_RAISED" />
            </stateChange>
        </eventHandler>
        <!-- case 7 : sched_switch : Fields: string prev_comm, int32 prev_tid,
            int32 prev_prio, int64 prev_state, string next_comm, int32 next_tid, int32
            next_prio -->
        <eventHandler eventName="sched_switch">
            <stateChange>
                <if>
                    <condition>
                        <field name="prev_state" />
                        <stateValue type="long"
                                    value="0" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="constant"
                                    value="Threads" />
                    <stateAttribute type="eventField"
                                    value="prev_tid" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$PROCESS_STATUS_WAIT_FOR_CPU" />
                </then>
                <else>
                    <stateAttribute type="constant"
                                    value="Threads" />
                    <stateAttribute type="eventField"
                                    value="prev_tid" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$PROCESS_STATUS_WAIT_BLOCKED" />
                </else>
            </stateChange>
            <stateChange>
                <if>
                    <condition>
                        <stateAttribute type="location"
                                        value="newCurrentThread" />
                        <stateAttribute type="constant"
                                        value="System_call" />
                        <stateValue type="null" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="location"
                                    value="newCurrentThread" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$PROCESS_STATUS_RUN_USERMODE" />
                </then>
                <else>
                    <stateAttribute type="location"
                                    value="newCurrentThread" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$PROCESS_STATUS_RUN_SYSCALL" />
                </else>
            </stateChange>
            <stateChange>
                <stateAttribute type="location"
                                value="newCurrentThread" />
                <stateAttribute type="constant"
                                value="Exec_name" />
                <stateValue type="eventField"
                            value="next_comm" />
            </stateChange>
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentCPU" />
                <stateAttribute type="constant"
                                value="Current_thread" />
                <stateValue type="eventField"
                            value="next_tid"
                            forcedType="int" />
            </stateChange>
            <stateChange>
                <if>
                    <not>
                        <condition>
                            <field name="next_tid" />
                            <stateValue type="long"
                                        value="0" />
                        </condition>
                    </not>
                </if>
                <then>
                    <if>
                        <condition>
                            <stateAttribute type="location"
                                            value="newCurrentThread" />
                            <stateAttribute type="constant"
                                            value="System_call" />
                            <stateValue type="null" />
                        </condition>
                    </if>
                    <then>
                        <stateAttribute type="location"
                                        value="CurrentCPU" />
                        <stateAttribute type="constant"
                                        value="Status" />
                        <stateValue type="int"
                                    value="$CPU_STATUS_RUN_USERMODE" />
                    </then>
                    <else>
                        <stateAttribute type="location"
                                        value="CurrentCPU" />
                        <stateAttribute type="constant"
                                        value="Status" />
                        <stateValue type="int"
                                    value="$CPU_STATUS_RUN_SYSCALL" />
                    </else>
                </then>
            </stateChange>
            <stateChange>
                <if>
                    <condition>
                        <field name="next_tid" />
                        <stateValue type="long"
                                    value="0" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="location"
                                    value="CurrentCPU" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$CPU_STATUS_IDLE" />
                </then>
            </stateChange>
        </eventHandler>
        <!-- case 8 : sched_process_fork : Fields: string parent_comm, int32 parent_tid,
            string child_comm, int32 child_tid -->
        <eventHandler eventName="sched_process_fork">
            <stateChange>
                <stateAttribute type="constant"
                                value="Threads" />
                <stateAttribute type="eventField"
                                value="child_tid" />
                <stateAttribute type="constant"
                                value="PPID" />
                <stateValue type="eventField"
                            value="parent_tid"
                            forcedType="int" />
            </stateChange>
            <stateChange>
                <stateAttribute type="constant"
                                value="Threads" />
                <stateAttribute type="eventField"
                                value="child_tid" />
                <stateAttribute type="constant"
                                value="Exec_name" />
                <stateValue type="eventField"
                            value="child_comm" />
            </stateChange>
            <stateChange>
                <stateAttribute type="constant"
                                value="Threads" />
                <stateAttribute type="eventField"
                                value="child_tid" />
                <stateAttribute type="constant"
                                value="Status" />
                <stateValue type="int"
                            value="$PROCESS_STATUS_WAIT_FOR_CPU" />
            </stateChange>
            <stateChange>
                <stateAttribute type="constant"
                                value="Threads" />
                <stateAttribute type="eventField"
                                value="child_tid" />
                <stateAttribute type="constant"
                                value="System_call" />
                <stateValue type="query">
                    <stateAttribute type="constant"
                                    value="Threads" />
                    <stateAttribute type="eventField"
                                    value="parent_tid" />
                    <stateAttribute type="constant"
                                    value="System_call" />
                </stateValue>
            </stateChange>
            <stateChange>
                <if>
                    <condition>
                        <stateAttribute type="constant"
                                        value="Threads" />
                        <stateAttribute type="eventField"
                                        value="child_tid" />
                        <stateAttribute type="constant"
                                        value="System_call" />
                        <stateValue type="null" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="constant"
                                    value="Threads" />
                    <stateAttribute type="eventField"
                                    value="child_tid" />
                    <stateAttribute type="constant"
                                    value="System_call" />
                    <stateValue type="string"
                                value="sys_clone" />
                </then>
            </stateChange>
        </eventHandler>
        <!-- case 10 : sched_process_free : Fields: string parent_comm, int32 parent_tid,
            string child_comm, int32 child_tid -->
        <eventHandler eventName="sched_process_free">
            <stateChange>
                <stateAttribute type="constant"
                                value="Threads" />
                <stateAttribute type="eventField"
                                value="tid" />
                <stateValue type="delete" />
            </stateChange>
        </eventHandler>
        <!-- case 11 : lttng_statedump_process_state : Fields: int32 type, int32
            mode, int32 pid, int32 submode, int32 vpid, int32 ppid, int32 tid, string
            name, int32 status, int32 vtid -->
        <eventHandler eventName="lttng_statedump_process_state">
            <stateChange>
                <if>
                    <condition>
                        <stateAttribute type="constant"
                                        value="Threads" />
                        <stateAttribute type="eventField"
                                        value="tid" />
                        <stateAttribute type="constant"
                                        value="Exec_name" />
                        <stateValue type="null" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="constant"
                                    value="Threads" />
                    <stateAttribute type="eventField"
                                    value="tid" />
                    <stateAttribute type="constant"
                                    value="Exec_name" />
                    <stateValue type="eventField"
                                value="name" />
                </then>
            </stateChange>
            <stateChange>
                <if>
                    <condition>
                        <stateAttribute type="constant"
                                        value="Threads" />
                        <stateAttribute type="eventField"
                                        value="tid" />
                        <stateAttribute type="constant"
                                        value="PPID" />
                        <stateValue type="null" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="constant"
                                    value="Threads" />
                    <stateAttribute type="eventField"
                                    value="tid" />
                    <stateAttribute type="constant"
                                    value="PPID" />
                    <stateValue type="eventField"
                                value="ppid"
                                forcedType="int" />
                </then>
            </stateChange>
            <stateChange>
                <if>
                    <and>
                        <condition>
                            <stateAttribute type="constant"
                                            value="Threads" />
                            <stateAttribute type="eventField"
                                            value="tid" />
                            <stateAttribute type="constant"
                                            value="Status" />
                            <stateValue type="null" />
                        </condition>
                        <condition>
                            <field name="status" />
                            <stateValue type="long"
                                        value="2" />
                        </condition>
                    </and>
                </if>
                <then>
                    <stateAttribute type="constant"
                                    value="Threads" />
                    <stateAttribute type="eventField"
                                    value="tid" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$PROCESS_STATUS_WAIT_FOR_CPU" />
                </then>
            </stateChange>
            <stateChange>
                <if>
                    <and>
                        <condition>
                            <stateAttribute type="constant"
                                            value="Threads" />
                            <stateAttribute type="eventField"
                                            value="tid" />
                            <stateAttribute type="constant"
                                            value="Status" />
                            <stateValue type="null" />
                        </condition>
                        <condition>
                            <field name="status" />
                            <stateValue type="long"
                                        value="5" />
                        </condition>
                    </and>
                </if>
                <then>
                    <stateAttribute type="constant"
                                    value="Threads" />
                    <stateAttribute type="eventField"
                                    value="tid" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$PROCESS_STATUS_WAIT_BLOCKED" />
                </then>
            </stateChange>
            <stateChange>
                <if>
                    <condition>
                        <stateAttribute type="constant"
                                        value="Threads" />
                        <stateAttribute type="eventField"
                                        value="tid" />
                        <stateAttribute type="constant"
                                        value="Status" />
                        <stateValue type="null" />
                    </condition>
                </if>
                <then>
                    <stateAttribute type="constant"
                                    value="Threads" />
                    <stateAttribute type="eventField"
                                    value="tid" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$PROCESS_STATUS_UNKNOWN" />
                </then>
            </stateChange>
        </eventHandler>
        <!-- case 12 : sched_wakeup : case 13 : sched_wakeup_new : Fields (same
            fields for both types): string comm, int32 tid, int32 prio, int32 success,
            int32 target_cpu -->
        <eventHandler eventName="sched_wakeup*">
            <stateChange>
                <if>
                    <and>
                        <not>
                            <condition>
                                <stateAttribute type="constant"
                                                value="Threads" />
                                <stateAttribute type="eventField"
                                                value="tid" />
                                <stateAttribute type="constant"
                                                value="Status" />
                                <stateValue type="int"
                                            value="$PROCESS_STATUS_RUN_USERMODE" />
                            </condition>
                        </not>
                        <not>
                            <condition>
                                <stateAttribute type="constant"
                                                value="Threads" />
                                <stateAttribute type="eventField"
                                                value="tid" />
                                <stateAttribute type="constant"
                                                value="Status" />
                                <stateValue type="int"
                                            value="$PROCESS_STATUS_RUN_SYSCALL" />
                            </condition>
                        </not>
                    </and>
                </if>
                <then>
                    <stateAttribute type="constant"
                                    value="Threads" />
                    <stateAttribute type="eventField"
                                    value="tid" />
                    <stateAttribute type="constant"
                                    value="Status" />
                    <stateValue type="int"
                                value="$PROCESS_STATUS_WAIT_FOR_CPU" />
                </then>
            </stateChange>
        </eventHandler>
        <!-- delfault : syscall -->
        <eventHandler eventName="sys_*">
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentThread" />
                <stateAttribute type="constant"
                                value="System_call" />
                <stateValue type="eventName" />
            </stateChange>
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentThread" />
                <stateAttribute type="constant"
                                value="Status" />
                <stateValue type="int"
                            value="$PROCESS_STATUS_RUN_SYSCALL" />
            </stateChange>
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentCPU" />
                <stateAttribute type="constant"
                                value="Status" />
                <stateValue type="int"
                            value="$CPU_STATUS_RUN_SYSCALL" />
            </stateChange>
        </eventHandler>
        <!-- delfault : compat_syscall -->
        <eventHandler eventName="compat_sys_*">
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentThread" />
                <stateAttribute type="constant"
                                value="System_call" />
                <stateValue type="eventName" />
            </stateChange>
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentThread" />
                <stateAttribute type="constant"
                                value="Status" />
                <stateValue type="int"
                            value="$PROCESS_STATUS_RUN_SYSCALL" />
            </stateChange>
            <stateChange>
                <stateAttribute type="location"
                                value="CurrentCPU" />
                <stateAttribute type="constant"
                                value="Status" />
                <stateValue type="int"
                            value="$CPU_STATUS_RUN_SYSCALL" />
            </stateChange>
        </eventHandler>
    </stateProvider>
</tmfxml>''',
    "Analyze KVM exit reasons and generate XY chart for exit reasons with extended elements and sub-elements.":'''<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <my id="extended.my"
        name="extended element 1">
        <mySubElement>Test</mySubElement>
        <mySubElement>Test2</mySubElement>
    </my>
    <xyView id="kernel.kvm.exit.xychart">
        <head>
            <analysis id="kernel.kvm.exit.sp" />
            <label value="Exit reasons" />
        </head>
        <entry path="Reasons/*"
               displayType="delta">
            <display type="self" />
        </entry>
    </xyView>
    <abc id="extended.abc"
         name="extended element abc">
        <mySubElement>Test</mySubElement>
        <mySubElement>Test2</mySubElement>
    </abc>
    <stateProvider id="kernel.kvm.exit.sp"
                   version="1">
        <head>
            <traceType id="org.eclipse.linuxtools.lttng2.kernel.tracetype" />
            <label value="KVM exit reasons" />
        </head>
        <!-- case 1 : exit_syscall : Fields: int64 ret -->
        <eventHandler eventName="kvm_exit">
            <stateChange>
                <stateAttribute type="constant"
                                value="Reasons" />
                <stateAttribute type="eventField"
                                value="exit_reason" />
                <stateValue type="int"
                            value="1"
                            increment="true" />
            </stateChange>
        </eventHandler>
    </stateProvider>
</tmfxml>''',
    "Analyze system call pattern for thread PID 8998, generate pattern segments, and update current thread on sched_switch events.":'''<?xml version="1.0" encoding="UTF-8"?>
<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <pattern version="0"
             id="syscall.analysis">
        <head>
            <traceType id="org.eclipse.linuxtools.lttng2.kernel.tracetype" />
            <label value="XML system call analysis" />
        </head>
        <!-- STORED FIELDS -->
        <storedField id="filename" />
        <storedField id="fd" />
        <storedField id="ret"
                     alias="ret" />
        <storedField id="flags"
                     alias="flags" />
        <storedField id="offset"
                     alias="offset" />
        <storedField id="fd_in"
                     alias="fd_in" />
        <storedField id="fd_out"
                     alias="fd_out" />
        <storedField id="uservaddr"
                     alias="uservaddr" />
        <storedField id="upeer_sockaddr"
                     alias="upeer_sockaddr" />
        <!-- SHORTCUTS -->
        <!-- Shorcut for the current running thread attribute -->
        <location id="CurrentThread">
            <stateAttribute type="constant"
                            value="Threads" />
            <stateAttribute type="query">
                <stateAttribute type="constant"
                                value="CPUs" />
                <stateAttribute type="eventField"
                                value="cpu" />
                <stateAttribute type="constant"
                                value="Current_thread" />
            </stateAttribute>
        </location>
        <!-- Shorcut for the current CPU attribute -->
        <location id="CurrentCPU">
            <stateAttribute type="constant"
                            value="CPUs" />
            <stateAttribute type="eventField"
                            value="cpu" />
        </location>
        <!-- The attribute initial specifies the FSMs that will be instanciated at the beginning of the analysis -->
        <patternHandler initial="sched_switch:syscall">
            <!-- CONDITIONS -->
            <!-- This condition check if the current running thread PID is 1311 -->
            <test id="tid_8998">
                <if>
                    <condition>
                        <stateValue type="query">
                            <stateAttribute type="location"
                                            value="CurrentCPU" />
                            <stateAttribute type="constant"
                                            value="Current_thread" />
                        </stateValue>
                        <stateValue type="long"
                                    value="8998" />
                    </condition>
                </if>
            </test>
            <!-- Test this : if ( !(1 ns < ts < 3 ns) || ((ts -state.syscall_entry_x.ts) < 3 ns) ) -->
            <test id="time_condition">
                <if>
                    <or>
                        <not>
                            <condition>
                                <timerange unit="ns">
                                    <in begin="1"
                                        end="3" />
                                </timerange>
                            </condition>
                        </not>
                        <condition>
                            <elapsedTime unit="ns">
                                <less since="syscall_entry_x"
                                      value="3" />
                            </elapsedTime>
                        </condition>
                    </or>
                </if>
            </test>
            <!-- Test if the current running thread PID is equal to the current scenario thread -->
            <test id="thread_thread">
                <if>
                    <condition>
                        <stateValue type="query">
                            <stateAttribute type="location"
                                            value="CurrentCPU" />
                            <stateAttribute type="constant"
                                            value="Current_thread" />
                        </stateValue>
                        <stateValue type="query">
                            <stateAttribute type="constant"
                                            value="#CurrentScenario" />
                            <stateAttribute type="constant"
                                            value="thread" />
                        </stateValue>
                    </condition>
                </if>
            </test>
            <!-- ACTIONS -->
            <!-- Generates three state changes in the state system -->
            <action id="sys_x_founded">
                <!-- Save the name of the system call executed under the current scenario path -->
                <stateChange>
                    <stateAttribute type="constant"
                                    value="#CurrentScenario" />
                    <stateAttribute type="constant"
                                    value="syscall" />
                    <stateAttribute type="constant"
                                    value="name" />
                    <stateValue type="eventName" />
                </stateChange>
                <!-- Save the value of the CPU under the current scenario path -->
                <stateChange>
                    <stateAttribute type="constant"
                                    value="#CurrentScenario" />
                    <stateAttribute type="constant"
                                    value="cpu" />
                    <stateValue type="eventField"
                                value="cpu" />
                </stateChange>
                <!-- Save the value of the current thread PID under the current scenario path -->
                <stateChange>
                    <stateAttribute type="constant"
                                    value="#CurrentScenario" />
                    <stateAttribute type="constant"
                                    value="thread" />
                    <stateValue type="query">
                        <stateAttribute type="location"
                                        value="CurrentCPU" />
                        <stateAttribute type="constant"
                                        value="Current_thread" />
                    </stateValue>
                </stateChange>
            </action>
            <!-- Generate a pattern segment -->
            <action id="exit_syscall_founded">
                <!-- Generate a pattern segment with the name of the system call  of the current scenario -->
                <segment>
                    <segType>
                        <segName>
                            <stateValue type="query">
                                <stateAttribute type="constant"
                                                value="#CurrentScenario" />
                                <stateAttribute type="constant"
                                                value="syscall" />
                                <stateAttribute type="constant"
                                                value="name" />
                            </stateValue>
                        </segName>
                    </segType>
                </segment>
            </action>
            <!-- FSMs -->
            <!-- System call FSM
		Declare an FSM to match all the system calls on thread 1311.
		The FSM will generate pattern segments that will represent the system calls found -->
            <fsm id="syscall"
                 initial="wait_syscall_entry_x">
                <!-- Validate that PID == 1311 before going to the initial state -->
                <initial>
                    <transition cond="tid_8998"
                                target="wait_syscall_entry_x" />
                </initial>
                <state id="wait_syscall_entry_x">
                    <!-- The state will stay here until we have a "syscall_entry_*" event -->
                    <transition event="sys_*"
                                target="syscall_entry_x"
                                action="sys_x_founded"
                                saveStoredFields="true" />
                </state>
                <state id="syscall_entry_x">
                    <!-- The state will stay here until we have a "syscall_exit_*" event -->
                    <transition event="exit_syscall"
                                cond="thread_thread"
                                target="syscall_exit_x"
                                action="exit_syscall_founded"
                                saveStoredFields="true"
                                clearStoredFields="true" />
                </state>
                <!-- The state will stay here forever -->
                <final id="syscall_exit_x" />
            </fsm>
            <!-- SCHED_SWITCH FSM ACTIONS -->
            <!-- Update the value of the current running thread -->
            <action id="update Current_thread">
                <stateChange>
                    <stateAttribute type="location"
                                    value="CurrentCPU" />
                    <stateAttribute type="constant"
                                    value="Current_thread" />
                    <stateValue type="eventField"
                                value="next_tid" />
                </stateChange>
            </action>
            <!-- sched_switch fsm
		Declare an FSM to update the value of the current thread running.
		The FSM will generate a state change to update the current thread, each time that it will meet a sched_switch event. -->
            <fsm id="sched_switch"
                 multiple="false">
                <!-- if event.name != sched_switch, no processing will be done -->
                <precondition event="sched_switch" />
                <initial>
                    <transition target="sched_switch" />
                </initial>
                <state id="sched_switch">
                    <!-- The state will stay here forever and execute the action "update current thread" each time a sched_switch event will be meet -->
                    <transition target="sched_switch"
                                action="update Current_thread" />
                </state>
            </fsm>
        </patternHandler>
    </pattern>
</tmfxml>''',
    "Test FSM to handle entry, action, and exit events within a time range, generate pattern segments for same CPU.":'''<?xml version="1.0" encoding="UTF-8"?>
<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <pattern version="0"
             id="xml.core.tests.simple.pattern">
        <head>
            <traceType id="org.eclipse.linuxtools.tmf.core.tests.xmlstub" />
            <label value="XML simple pattern test" />
        </head>
        <!-- the pattern handler specifies the FSM that will be instanciated at the beginning of the analysis -->
        <patternHandler initial="testTimeConditions">
            <!-- CONDITIONS -->
            <test id="sameCpu">
                <if>
                    <condition>
                        <stateAttribute type="constant"
                                        value="#CurrentScenario" />
                        <stateAttribute type="constant"
                                        value="cpu" />
                        <stateValue type="eventField"
                                    value="cpu" />
                    </condition>
                </if>
            </test>
            <test id="timeRange">
                <if>
                    <condition>
                        <timerange unit="ns">
                            <in begin="5"
                                end="20" />
                        </timerange>
                    </condition>
                </if>
            </test>
            <test id="smallExec">
                <if>
                    <condition>
                        <elapsedTime unit="ns">
                            <less since="waitEnd"
                                  value="4" />
                        </elapsedTime>
                    </condition>
                </if>
            </test>
            <!-- ACTIONS -->
            <action id="startEvent">
                <stateChange>
                    <stateAttribute type="constant"
                                    value="#CurrentScenario" />
                    <stateAttribute type="constant"
                                    value="cpu" />
                    <stateValue type="eventField"
                                value="cpu" />
                </stateChange>
                <stateChange>
                    <stateAttribute type="constant"
                                    value="CPU" />
                    <stateAttribute type="eventField"
                                    value="cpu" />
                    <stateValue type="int"
                                value="1" />
                </stateChange>
            </action>
            <action id="incrementEvents">
                <stateChange>
                    <stateAttribute type="constant"
                                    value="CPU" />
                    <stateAttribute type="eventField"
                                    value="cpu" />
                    <stateValue type="int"
                                value="1"
                                increment="true" />
                </stateChange>
            </action>
            <action id="doSegment">
                <!-- Generate a pattern segment with the name 'test2' and with three fields 'field1', 'field2' and 'field2' -->
                <segment>
                    <segType>
                        <segName>
                            <stateValue type="query">
                                <stateAttribute type="constant"
                                                value="CPUs" />
                                <stateAttribute type="query">
                                    <stateAttribute type="constant"
                                                    value="#CurrentScenario" />
                                    <stateAttribute type="constant"
                                                    value="cpu" />
                                </stateAttribute>
                            </stateValue>
                        </segName>
                    </segType>
                </segment>
            </action>
            <action id="resetCount">
                <stateChange>
                    <stateAttribute type="constant"
                                    value="CPU" />
                    <stateAttribute type="eventField"
                                    value="cpu" />
                    <stateValue type="delete" />
                </stateChange>
            </action>
            <!-- FSMs -->
            <!-- test fsm
		Declare a test FSM that that will generate two segments for each event received -->
            <fsm id="testTimeConditions"
                 multiple="true"
                 initial="waitBegin">
                <state id="waitBegin">
                    <!-- wait for an entry event within time range -->
                    <transition event="entry"
                                cond="timeRange"
                                target="waitEnd"
                                action="startEvent" />
                </state>
                <state id="waitEnd">
                    <!-- wait for exit, will create segment only longer than 5 -->
                    <transition event="action"
                                cond="sameCpu"
                                target="waitEnd"
                                action="incrementEvents" />
                    <transition event="exit"
                                cond="sameCpu:smallExec"
                                target="endTest"
                                action="doSegment:resetCount" />
                    <transition event="exit"
                                cond="sameCpu"
                                target="endTest"
                                action="resetCount" />
                </state>
                <final id="endTest" />
            </fsm>
        </patternHandler>
    </pattern>
</tmfxml>''',
    "Create a TimeGraphView for 'Xml Timegraph View Test' with state values 'NONE' and 'VALID' and a display entry for 'checkpoint'.":'''<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <timeGraphView id="org.eclipse.linuxtools.tmf.analysis.xml.ui.views.controlflow">
        <head>
            <analysis id="test.xml.conditions" />
            <label value="Xml Timegraph View Test" />
        </head>
        <!-- StateValues -->
        <definedValue name="NONE"
                      value="0"
                      color="#EEEEEE" />
        <definedValue name="VALID"
                      value="1"
                      color="#FF0000" />
        <entry path="checkpoint"
               displayText="true">
            <display type="self" />
        </entry>
    </timeGraphView>
</tmfxml>''',
    "Show me the irqs vs time where you store the irq name it should be categorized by a tid.": '''<?xml version="1.0" encoding="UTF-8"?>
    <tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
        <timeGraphView id="xml.scenarios">
            <head>
                <analysis id="lttng.analysis.irq" />
                <label value="Scenarios" />
            </head>
            <definedValue name="PENDING" value="0" color="#CCCCCC" />
            <definedValue name="IN_PROGRESS" value="1" color="#00CCFF" />
            <definedValue name="MATCHED" value="2" color="#118811" />
            <definedValue name="ABANDONED" value="3" color="#EE0000" />
            <entry path="scenarios/*">
                <display type="self" />
                <name type="self" />
                <entry path="*">
                    <display type="constant" value="state" />
                    <name type="self" />
                </entry>
            </entry>
        </timeGraphView>
        <pattern version="0" id="lttng.analysis.irq">
            <head>
                <traceType id="org.eclipse.linuxtools.lttng2.kernel.tracetype" />
                <label value="IRQ Analysis"/>
                <viewLabelPrefix value="IRQ" />
            </head>
            <storedField id="ret" alias="ret" />
            <location id="CurrentCPU">
                <stateAttribute type="constant" value="CPUs" />
                <stateAttribute type="eventField" value="cpu" />
            </location>
            <patternHandler>
                <test id="test_cpu">
                    <if>
                        <condition>
                            <stateValue type="query">
                                <stateAttribute type="constant" value="#CurrentScenario" />
                                <stateAttribute type="constant" value="cpu" />
                            </stateValue>
                            <stateValue type="eventField" value="cpu" />
                        </condition>
                    </if>
                </test>
                <action id="irq_handler_entry">
                    <stateChange>
                        <stateAttribute type="constant" value="#CurrentScenario" />
                        <stateAttribute type="constant" value="irq" />
                        <stateValue type="eventField" value="irq" />
                    </stateChange>
                    <stateChange>
                        <stateAttribute type="constant" value="#CurrentScenario" />
                        <stateAttribute type="constant" value="name" />
                        <stateValue type="eventField" value="name" />
                    </stateChange>
                    <stateChange>
                        <stateAttribute type="constant" value="#CurrentScenario" />
                        <stateAttribute type="constant" value="cpu" />
                        <stateValue type="eventField" value="cpu" />
                    </stateChange>
                </action>
                <action id="irq_handler_exit">
                    <segment>
                        <segType>
                            <segName>
                                <stateValue type="query">
                                    <stateAttribute type="constant" value="#CurrentScenario" />
                                    <stateAttribute type="constant" value="name" />
                                </stateValue>
                            </segName>
                        </segType>
                        <segContent>
                            <segField name="ret" type="long">
                                <stateValue type="eventField" value="ret" />
                            </segField>
                            <segField name="irq" type="long">
                                <stateValue type="query">
                                    <stateAttribute type="constant" value="#CurrentScenario" />
                                    <stateAttribute type="constant" value="irq" />
                                </stateValue>
                            </segField>
                            <segField name="cpu" type="long">
                                <stateValue type="eventField" value="cpu" />
                            </segField>
                        </segContent>
                    </segment>
                </action>
                <fsm id="irq_handler" initial="wait_irq_entry">
                    <precondition event="irq_handler_*" />
                    <state id="wait_irq_entry">
                        <transition event="irq_handler_entry" target="wait_irq_exit"
                            action="irq_handler_entry" />
                    </state>
                    <state id="wait_irq_exit">
                        <transition event="irq_handler_exit" cond="test_cpu"
                            target="irq" action="irq_handler_exit" />
                    </state>
                    <final id="irq" />
                </fsm>
                <action id="update_current_thread">
                    <stateChange>
                        <stateAttribute type="location" value="CurrentCPU" />
                        <stateAttribute type="constant" value="Current_thread" />
                        <stateValue type="eventField" value="next_tid" />
                    </stateChange>
                </action>
                <fsm id="sched_switch" multiple="false">
                    <precondition event="sched_switch" />
                    <state id="sched_switch">
                        <transition event="sched_switch" target="sched_switch"
                            action="update_current_thread" />
                    </state>
                </fsm>
            </patternHandler>
        </pattern>
    </tmfxml>'''
}
# Function to extract key tags and keywords from XML content
def extract_key_tags_and_keywords_from_xml(xml_content):
    tree = ET.ElementTree(ET.fromstring(xml_content))
    root = tree.getroot()
    
    key_tags = set()
    keywords = set()
    
    def traverse(element):
        key_tags.add(element.tag)
        keywords.update(element.attrib.keys())
        keywords.update(element.attrib.values())
        if element.text and element.text.strip():
            keywords.update(element.text.strip().split())
        for child in element:
            traverse(child)
    
    traverse(root)
    return list(key_tags), list(keywords)

# Extract key tags and keywords from the XML dataset
def extract_key_tags_and_keywords_from_dataset(dataset):
    key_tags_set = set()
    keywords_set = set()
    for xml in dataset.values():
        key_tags, keywords = extract_key_tags_and_keywords_from_xml(xml)
        key_tags_set.update(key_tags)
        keywords_set.update(keywords)
    return list(key_tags_set), list(keywords_set)

# Extract key tags and keywords from the dataset
key_tags, keywords = extract_key_tags_and_keywords_from_dataset(prompts_xml_mapping)

# Save the key tags and keywords to a JSON file
output_data = {
    "key_tags": key_tags,
    "keywords": keywords
}
output_file_path = "key_tags_and_keywords.json"
with open(output_file_path, "w") as f:
    json.dump(output_data, f, indent=4)

print(f"Key tags and keywords have been saved to {output_file_path}")
