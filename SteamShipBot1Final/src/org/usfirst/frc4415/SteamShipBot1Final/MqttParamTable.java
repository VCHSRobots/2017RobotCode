// --------------------------------------------------------------------
// MqttMessageArrived.java -- Manages parameter tables with MQTT
//
// Created 03/23/17 DLB
// -------------------------------------------------------------------

package org.usfirst.frc4415.SteamShipBot1Final;

import java.util.HashMap;
import java.util.Map;

public class MqttParamTable implements MqttMessageArrived {

	private Mqtt m_mqtt;
	private Map<String, Double> m_data = new HashMap<String, Double>();;
	private String paramDefaults = 
			"ssy0=-300; ssr0=1000" +
			"ssy1=-281; ssr1=1010" +
			"ssy2=-200; ssr2=1050" +
			"ssy3=-133; ssr3=1070" +
			"ssy4=-72;  ssr4=1125" +
			"ssy5=-30;  ssr5=1200" +	
			"ssy6=121;  ssr6=1200" ;
			
	
	public MqttParamTable(Mqtt mqtt) {
		m_mqtt = mqtt;
		m_mqtt.NotifyOnNewMessage(this);
		LoadDefaults();
	}
	
	private void LoadParams(String data) {
		m_data.clear();
		String[] lines = data.split(";");
		for(String x: lines) {
			String[] parts = x.split("=");
			if (parts.length != 2) continue;
			String key = parts[1];
			double val = 0.0;
			try {
				val = Double.parseDouble(parts[2]);
			}
			catch (NumberFormatException ee) {
				continue;
			}
			m_data.put(key,  val);
		}
	}
	
	// Loads the defaults
	public void LoadDefaults() {
		LoadParams(paramDefaults);
	}
	
	// Gets the param.  If doesn't exist, returns the given default.
	public double getParam(String key, double defalutval) {
		if (m_data.containsKey(key)) {
			return m_data.get(key);
		}
		return defalutval;
	}
	
	// Gets the param.  If doesn't exist zero is returned.
	public double getParam(String key) 
	{
		return getParam(key, 0.0);
	}
	
	public void setParam(String key, double val) {
		m_data.put(key, val);
	}
	
	// Callback to process new messages.
	public void OnNewMessage(MqttMsg m) {

		if (m.getTopic().equals("robot/ds/rio/tableparams")) {
			return;
		}
		
		if (m.getTopic().equals("robot/ds/rio/sendtableparams")) {
			String sdata = "";
			for (String key : m_data.keySet()) {
			    double dval = m_data.get(key);
			    String s = String.format("%s=%12.6f;", key, dval);
			    sdata += s;
			}
			m_mqtt.sendMessage("robot/roborio/tableparams", sdata);
			return;
		}	
		
		if (m.getTopic().equals("robot/ds/rio/usetabledefaults")) {
			Robot.logf("Got Default Msg");
			LoadDefaults();
			return;
		}		
	}	
}
