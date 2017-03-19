package org.usfirst.frc4415.SteamShipBot1Final;
import com.ctre.CANTalon;

public class PIDCANTalonPosition extends PIDController{
	
	private CANTalon motor;
	
	public PIDCANTalonPosition(CANTalon motor, 
			double setpoint, double threshold, 
			long timeout){
		super(setpoint, threshold, timeout);
		this.motor = motor;
	}
	
	public void run(){
		motor.set(super.calculateActuatorValue(
				motor.getEncPosition()));
	}
}