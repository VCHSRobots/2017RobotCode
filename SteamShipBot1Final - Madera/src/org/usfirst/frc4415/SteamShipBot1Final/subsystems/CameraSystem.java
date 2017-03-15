// RobotBuilder Version: 2.0
//
// This file was generated by RobotBuilder. It contains sections of
// code that are automatically generated and assigned by robotbuilder.
// These sections will be updated in the future when you export to
// Java from RobotBuilder. Do not put any code or make any change in
// the blocks indicating autogenerated code or it will be lost on an
// update. Deleting the comments indicating the section will prevent
// it from being updated in the future.


package org.usfirst.frc4415.SteamShipBot1Final.subsystems;

import org.usfirst.frc4415.SteamShipBot1Final.RobotMap;
import org.usfirst.frc4415.SteamShipBot1Final.commands.*;

import edu.wpi.first.wpilibj.DigitalOutput;
import edu.wpi.first.wpilibj.Servo;
import edu.wpi.first.wpilibj.command.Subsystem;


/**
 *
 */
public class CameraSystem extends Subsystem {

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTANTS

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTANTS
	
	boolean toggleAngle = false; 
	double cameraX = .486;
	double cameraY = .314;
	double delta = 0.008;
	
    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DECLARATIONS
    private final Servo servo = RobotMap.cameraSystemServo;
    private final Servo servo2 = RobotMap.cameraSystemServo2;
    private final DigitalOutput lED = RobotMap.cameraSystemLED;

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DECLARATIONS


    // Put methods for controlling this subsystem
    // here. Call these from Commands.

    public void initDefaultCommand() {
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DEFAULT_COMMAND

        setDefaultCommand(new CameraSystemDefault());

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DEFAULT_COMMAND

        // Set the default command for a subsystem here.
        // setDefaultCommand(new MySpecialCommand());
    }
    
    public void toggleCameraAngle(){
    	toggleAngle = !toggleAngle;
    	if(toggleAngle){
    		servo.set(0.314);
    		servo2.set(0.486);
    	} else {
    		servo.set(0.161);
    		servo2.set(.67);
    	}
    }
    
    public boolean getLED(){
    	return lED.get();
    }
    
    public void ledOff(){
    	lED.set(false);
    }
    
    public void ledToggle(){
    	lED.set(!lED.get());
    }
    
    public void setServo1(double position) {
    	servo.set(position);
    }
    
    public void setServo2(double position) {
    	servo2.set(position);
    }
    
    public void incServo1(){
    	cameraY += delta;
    	servo.set(cameraY);
    	if(cameraY > 1) cameraY = 1;
    }
    
    public void decServo1(){
    	cameraY -= delta;
    	servo.set(cameraY);
    	if(cameraY < -1) cameraY = -1;
    }
    
    public void incServo2(){
    	cameraX += delta;
    	servo2.set(cameraX);
    	if(cameraX > 1) cameraX = 1;
    }
    
    public void decServo2(){
    	cameraX -= delta;
    	servo2.set(cameraX);
    	if(cameraX < -1) cameraX = -1;
    }
    
    public double getY(){
    	return cameraY;
    }
    
    public double getX(){
    	return cameraX;
    }
    
    
}
