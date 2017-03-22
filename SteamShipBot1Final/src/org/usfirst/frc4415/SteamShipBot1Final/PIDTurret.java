/*-------------------------------------------------------
 * 
 * PIDTurret
 * 
 * Created by Kyle Fleming, 3/18/2017
 * 
 *///----------------------------------------------------
package org.usfirst.frc4415.SteamShipBot1Final;

import org.usfirst.frc4415.SteamShipBot1Final.subsystems.Turret;

public class PIDTurret extends PIDController{
	
	private Turret turret;
	
	public PIDTurret(
			Turret turret,
			double setpoint,
			double threshold,
			long timeout
			){
		super(setpoint, false, threshold, timeout);
		this.turret = turret;
	}
	
	public void run(double feedback){
		turret.turn(super.calculateActuatorValue(feedback));
	}
}