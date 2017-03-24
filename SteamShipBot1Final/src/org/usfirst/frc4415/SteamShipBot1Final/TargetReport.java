// --------------------------------------------------------------------
// TargetReport.java -- Contains a single report from the targeting system.
//
// Created 03/22/17 DLB
// --------------------------------------------------------------------

package org.usfirst.frc4415.SteamShipBot1Final;

import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class TargetReport  {

	private MqttMsg m_msg = null;
	private int m_iMode = 0;
	private boolean m_Valid = false;
	private double m_dX = 0.0;
	private double m_dY = 0.0;
	private double m_dX1 = 0.0;
	private double m_dY1 = 0.0;
	private double m_dH1 = 0.0;
	private double m_dW1 = 0.0;
	private double m_dX2 = 0.0;
	private double m_dY2 = 0.0;
	private double m_dH2 = 0.0;
	private double m_dW2 = 0.0;
	private boolean m_error = false;
	
	public TargetReport()
	{
	}
	
	public TargetReport(MqttMsg m)
	{
		m_msg = m;
		LoadData();
	}
	
	public MqttMsg msg() {
		if(m_msg == null) {
			MqttMsg m = new MqttMsg("", "");
			return m;
		}
		return m_msg;
	}
	
	public long age() {
		if(m_msg != null) {
			return m_msg.getAge();
		}
		return 10000;
	}
	
	public boolean isValid() {
		return m_Valid;
	}
		
	public int mode() {
		return m_iMode;
	}
	
	public double x1000() {
		return m_dX;
	}
	
	public double y1000() {
		return m_dY;
	}
	
	public double x1() {
		return m_dX1;
	}
	
	public double y1() {
		return m_dY1;
	}
	
	public double h1() {
		return m_dH1;
	}
	
	public double w1() {
		return m_dW1;
	}
	
	public double x2() {
		return m_dX1;
	}
	
	public double y2() {
		return m_dY2;
	}
	
	public double h2() {
		return m_dH2;
	}
	
	public double w2() {
		return m_dW2;
	}
	
	public boolean error() {
		return m_error;
	}
	
	private void LoadData() {
		String data = m_msg.getMessage();
		String[] vals = data.split(";");
		for(String v: vals) {
			String[] parts = v.split("=");
			if (parts.length != 2) continue;
			String key = parts[0].trim();
			String sval = parts[1].trim();
			double dval = 0.0;
			try {
				dval = Double.parseDouble(sval);
			}
			catch (NumberFormatException ee) {
				m_error = true;
				m_Valid = false;
				return;
			}
			if (key.equals("Mode")) {
				try {
					m_iMode = Integer.parseInt(sval);
					if(m_iMode <= 0) {
						m_Valid = false;
					}
				}
				catch (NumberFormatException ee) {
					m_error = true;
					m_Valid = false;
					return;
				}
			}
			if (key.equals("Valid")) {
				if(dval > 0.0) m_Valid = true;
				else m_Valid = false;
			}
			if (key.equals("X")) {
				m_dX = dval;
			}
			if (key.equals("Y")) {
				m_dY = dval;
			}
			if (key.equals("x1")) {
				m_dX1 = dval;
			}
			if (key.equals("y1")) {
				m_dY1 = dval;
			}			
			if (key.equals("w1")) {
				m_dW1 = dval;
			}
			if (key.equals("h1")) {
				m_dH1 = dval;
			}
			if (key.equals("x2")) {
				m_dX2 = dval;
			}
			if (key.equals("y2")) {
				m_dY2 = dval;
			}			
			if (key.equals("w2")) {
				m_dW2 = dval;
			}
			if (key.equals("h2")) {
				m_dH2 = dval;
			}
		}
	}
}
