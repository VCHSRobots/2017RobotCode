// --------------------------------------------------------------------
// TargetReportMonitor.java -- Monitors for MQTT target messages.
//
// Created 03/22/17 DLB
// --------------------------------------------------------------------

package org.usfirst.frc4415.SteamShipBot1Final;


public class TargetReportMonitor implements MqttMessageArrived {

	private Mqtt m_mqtt;
	private TargetReport m_LastGoodReport = new TargetReport();
	
	private int m_nCountInValids = 0;
	private int m_nCountErrors = 0;
	private int m_nCountMsg = 0;
	private int m_nCountUpdates = 0;

	public void selectTarget(int imode) {
		String s = String.format("%d", imode);
		m_mqtt.sendMessage("robot/roborio/targetmode", s);
	}
	
	public TargetReportMonitor(Mqtt mqtt) {
		m_mqtt = mqtt;
		m_mqtt.NotifyOnNewMessage(this);
	}
	
	public int countInvalid() {
		return m_nCountInValids;
	}
	
	public int countErrors() {
		return m_nCountErrors;
	}
	
	public int countMsg() {
		return m_nCountMsg;
	}
	
	public int countUpdates() {
		return m_nCountUpdates;
	}
	
	// Status is False if we haven't got targeting info. Or if the
	// targeting info is older than 2 seconds...
	public boolean getStatus() {
		if(m_LastGoodReport == null) return false;
		if(m_LastGoodReport.age() > 2000) return false;
		return true;
	}
	
	// Gets the latest good report here.
	public TargetReport report() {
		return m_LastGoodReport;
	}
	
	// Callback to process new messages.
	public void OnNewMessage(MqttMsg m) {

		if (!m.getTopic().equals("robot/jetson/targetreport")) {
			return;
		}
		m_nCountMsg++;
		TargetReport r = new TargetReport(m);
		if (r.isValid()) {
			m_LastGoodReport  = r;
			m_nCountUpdates++;
			m_nCountInValids = 0;
		}
		else {
			m_nCountInValids++;
		}
	}
}
