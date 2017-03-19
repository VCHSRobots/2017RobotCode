/*-------------------------------------------------------
 * 
 * PIDRobotDriveRotate - Running an instance of this 
 * 						class will rotate a RobotDrive 
 * 						object to a setpoint using a 
 * 						navX gyro
 * 
 * Created by Kyle Fleming, 3/18/2017
 * 
 * Requirements: 
 * 		1. The gyro MUST go in the 
 * 			same direction as the RobotDrive.
 * 			i.e. if RobotDrive is given
 * 			a positive setpoint, the gyro
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

import com.kauailabs.navx.frc.AHRS;
import edu.wpi.first.wpilibj.RobotDrive;

public class PIDRobotDriveRotate extends PIDController{
	
	private RobotDrive robotDrive;
	private AHRS navX;
	
	public PIDRobotDriveRotate(
			RobotDrive robotDrive,
			AHRS navX,
			double setpoint, 
			double threshold,
			long timeout
			){
		super(setpoint, threshold, timeout);
		this.robotDrive = robotDrive;
		this.navX = navX;
	}
	
	public void run(){
		robotDrive.arcadeDrive(
				0,
				super.calculateActuatorValue(
						navX.getAngle())
				);
	}
}