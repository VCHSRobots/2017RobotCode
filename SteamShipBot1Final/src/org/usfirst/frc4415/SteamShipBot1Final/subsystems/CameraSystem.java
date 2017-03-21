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
	double cameraX = .594;				// was .486
	double cameraY = .101999999;				// was .314
	double delta = 0.008;
	
    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DECLARATIONS
    private final Servo servo1 = RobotMap.cameraSystemServo1;
    private final Servo servo2 = RobotMap.cameraSystemServo2;
    private final DigitalOutput lED = RobotMap.cameraSystemLED;
    private final DigitalOutput pin1 = RobotMap.cameraSystemPin1;
    private final DigitalOutput pin2 = RobotMap.cameraSystemPin2;
    private final DigitalOutput pin3 = RobotMap.cameraSystemPin3;
    private final DigitalOutput pin4 = RobotMap.cameraSystemPin4;

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
    		servo1.set(0.314);
    		servo2.set(0.486);
    	} else {
    		servo1.set(0.161);				// was .161
    		servo2.set(.67);				// was .67
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
    	servo1.set(position);
    }
    
    public void setServo2(double position) {
    	servo2.set(position);
    }
    
    public void incServo1(){
    	cameraY += delta;
    	servo1.set(cameraY);
    	if(cameraY > 1) cameraY = 1;
    }
    
    public void decServo1(){
    	cameraY -= delta;
    	servo1.set(cameraY);
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
    
    //LED Code for Robot Orientation
    
    /*public void setPin1Low() {
    	pin1.set(false);
    }
    
    public void setPin1High() {
    	pin1.set(true);
    }
    
    public void setPin2Low() {
    	pin2.set(false);
    }
    
    public void setPin2High() {
    	pin2.set(true);
    }
    
    public void setPin3Low() {
    	pin3.set(false);
    }
    
    public void setPin3High() {
    	pin3.set(true);
    }
    
    public void setPin4Low() {
    	pin4.set(false);
    }
    
    public void setPin4High() {
    	pin4.set(true);
    }*/
    
    public boolean getPin1() {
    	return pin1.get();
    }
    
    public boolean getPin2() {
    	return pin2.get();
    }
    
    public boolean getPin3() {
    	return pin3.get();
    }
    
    public boolean getPin4() {
    	return pin4.get();
    }
    
    // Solid Green
    public void program1() {
    	pin1.set(false);
    	pin2.set(false);
    	pin3.set(false);
    	pin4.set(true);
    }
    
    // Solid Red
    public void program2() {
    	pin1.set(false);
    	pin2.set(false);
    	pin3.set(true);
    	pin4.set(false);
    }
    
    // Moving Green
    public void program3() {
    	pin1.set(false);
    	pin2.set(false);
    	pin3.set(true);
    	pin4.set(true);
    }
    
    // Moving Red
    public void program4() {
    	pin1.set(false);
    	pin2.set(true);
    	pin3.set(false);
    	pin4.set(true);
    }
    
    // Shooter
    public void program5() {
    	pin1.set(false);
    	pin2.set(true);
    	pin3.set(false);
    	pin4.set(true);
    }
    
    // Climber
    public void program6() {
    	pin1.set(false);
    	pin2.set(true);
    	pin3.set(true);
    	pin4.set(false);
    }
    
    // Lights Off
    public void program7() {
    	pin1.set(false);
    	pin2.set(true);
    	pin3.set(false);
    	pin4.set(true);
    }
    
}

