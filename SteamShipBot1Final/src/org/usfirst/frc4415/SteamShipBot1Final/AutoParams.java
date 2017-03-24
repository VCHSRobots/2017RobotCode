// --------------------------------------------------------------------
// AudoParams.java -- Class to get parameters for autonomous mode
//
// Created 3/20/17 DLB
// --------------------------------------------------------------------

package org.usfirst.frc4415.SteamShipBot1Final;

// Class to deal with getting the parameters for autonomous mode
// Please see C# program for possibilities.  Currently for 
// program, these are:
// MoveForward, CenterGear, GearAndShoot, SideGearAndShoot, BinAndShoot
// 
// For Sides: red, blue.
//

public class AutoParams {
	
	private Mqtt m_mqtt;
	private String m_side  = "blue";
	private String m_program = "MoveForward";
	private boolean m_usingDefaults = true;
	
	public AutoParams(Mqtt mqtt) {
		m_mqtt = mqtt;
		loadData();
	}
	
	public void loadData() {
		int nCount = 0;
		int nChange = 0;
		MqttMsg m = m_mqtt.getMessage("robot/ds/autoside");
		if(m != null) {
			String newside = m.getMessage();
			if(!newside.equals(m_side)) nChange++;
			m_side = newside;
			nCount++;
		}	
		m = m_mqtt.getMessage("robot/ds/autoprogram");
		if(m != null) {
			String newprogram = m.getMessage();
			if(!newprogram.equals(m_program)) nChange++;
			m_program =newprogram;
			nCount++;
		}
		if (nCount >= 2) m_usingDefaults = false;
		else m_usingDefaults = true;
		String ff = "false";
		if (isDefaults()) { ff = "true"; }
		if (nChange > 0 ) m_mqtt.logf("New Auto Program Parameters Loaded! side=%s, program=%s", getSide(), getProgram());
		//System.out.format("\nAudoParams Loaded:  nCount=%d\n", nCount);
		//m_mqtt.logf("Auto Params Read: side=%s, pgm=%s, IsDefault=%s", getSide(), getProgram(), ff);
	}
	
	public String getSide() {
		return m_side;
	}
	
	public String getProgram() {
		return m_program;
	}
	
	public boolean isDefaults()
	{
		return m_usingDefaults;
	}
}
