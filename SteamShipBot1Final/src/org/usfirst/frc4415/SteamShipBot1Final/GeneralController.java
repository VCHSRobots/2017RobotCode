/*
 * GeneralController.java
 * 
 * Created 3/23/2017 - KJF
*/
package org.usfirst.frc4415.SteamShipBot1Final;

public class GeneralController {
	public GeneralController(){}
	public void run(double feedback){}
	public boolean isDone(){
		return true;
	}
	public void setPGain(double pGain){}
	
	public void setIGain(double iGain){}
	
	public void setDGain(double dGain){}
	
	public double getPTerm(){
		return 0;
	}
	
	public double getITerm(){
		return 0;
	}
	
	public double getDTerm(){
		return 0;
	}
	
	public double getDeadbandTerm(){
		return 0;
	}
	
	public void setClipping(double clipping){}
	
	public void setDeadband(double deadband){}
	
	public void setSetpoint(double setpoint){}
	
	public void setThreshold(double threshold){}
	
	public void setThresholdLoop(int thresholdLoop){}
	
	public void setTimeout(long timeout){}	
	
	public double getActuatorValue(){
		return 0;
	}
}