/*-------------------------------------------------------
 * 
 * PIDRobotDriveMove - Running an instance of this class
 * 						will drive a RobotDrive object
 * 						to a setpoint using an encoder
 * 						plugged into the roboRIO
 * 
 * Created by Kyle Fleming, 3/18/2017
 * 
 * Requirements: 
 * 		1. The encoder MUST go in the 
 * 			same direction as the RobotDrive.
 * 			i.e. if RobotDrive is given
 * 			a positive setpoint, the encoder
 * 			should count in the positive direction
 * 		2. For integral control, the RobotDrive must 
 * 			cross the setpoint.
 * 			
 * 
 * Directions: 
 * 		1. To determine the deadband, manually
 * 			increase the value given to the RobotDrive
 * 			until the robot physically begins 
 * 			moving.  Set the deadband to this value.
 * 		2. Set the RobotDrive to a positive value.  
 * 			Check that the encoder is changing in the 
 * 			positive direction.  If not, correct.
 * 
 *///----------------------------------------------------
package org.usfirst.frc4415.SteamShipBot1Final;

import edu.wpi.first.wpilibj.Encoder;
import edu.wpi.first.wpilibj.RobotDrive;

public class PIDRobotDriveMove extends PIDController{
	
	private RobotDrive robotDrive;
	private Encoder encoder;
	
	public PIDRobotDriveMove(
			RobotDrive robotDrive,
			Encoder encoder,
			double setpoint, 
			double threshold,
			long timeout
			){
		super(setpoint, threshold, timeout);
		this.robotDrive = robotDrive;
		this.encoder = encoder;
	}
	
	public void run(){
		robotDrive.arcadeDrive(
				super.calculateActuatorValue(
						encoder.get()),
				0);
	}
}