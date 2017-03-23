//
// This file was generated by RobotBuilder. It contains sections of
// code that are automatically generated and assigned by robotbuilder.
// These sections will be updated in the future when you export to
// Java from RobotBuilder. Do not put any code or make any change in
// the blocks indicating autogenerated code or it will be lost on an
// update. Deleting the comments indicating the section will prevent
// it from being updated in the future.


package org.usfirst.frc4415.SteamShipBot1Final.commands;
import edu.wpi.first.wpilibj.Timer;
import edu.wpi.first.wpilibj.command.Command;

import org.usfirst.frc4415.SteamShipBot1Final.Robot;

/**
 *
 */
public class AutoShootWithoutTarget extends Command {

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_DECLARATIONS
 
    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_DECLARATIONS

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTOR
    public AutoShootWithoutTarget() {

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTOR
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_SETTING

        // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_SETTING
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=REQUIRES

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=REQUIRES
    }

    // Called just before this Command runs the first time
    protected void initialize() {
    	
    	Robot.driveTrain.setArcade();
    	Robot.gearHandler.gearGrab();
    	Robot.gearHandler.handlerOut();

    	long startTime = System.currentTimeMillis();
    	
      	while (System.currentTimeMillis() - startTime < 1300) {						//from 1000 to 1300
    		Robot.driveTrain.set(.6);
    		Timer.delay(0.01);
    	}
    	
    	startTime = System.currentTimeMillis();
    	while (Robot.driveTrain.getIR() < 900 && System.currentTimeMillis() - startTime < 2000) {	//950 to 900		// from 3000 to 2000
    		Robot.driveTrain.set(.4);
    		Timer.delay(.01);
    	}
    	
    	Robot.gearHandler.gearRelease();
    	
    	Timer.delay(.4);									// from .5 to .4
    	Robot.gearHandler.handlerIn();
    	Timer.delay(.4);									// from .5 to .4
    	
    	Robot.shooter.setSetpoint(Robot.tableReader.get("shootersetpoint", 2825));
    	Robot.shooter.toggleShooter();
    	
    	Robot.driveTrain.arcadePIDMove(Robot.tableReader.get("pidmove1", -20), 4000);									
    	
    	//red alliance is boiler left and gear dispenser right
    	//blue alliance is boiler right and gear dispenser left
    	
    	Robot.driveTrain.arcadePIDRotate(Robot.tableReader.get("pidrotate1", 71), 1000);    //for red alliance use -68
    	
    	Robot.driveTrain.arcadePIDMove(Robot.tableReader.get("pidmove2", -53), 4000);  //for red alliance use -58
    	
    	Robot.blender.set(-1);
    	Timer.delay(7);
    	
    	Robot.shooter.toggleShooter();

    }
    
    // Called repeatedly when this Command is scheduled to run
    protected void execute() {

    }

    // Make this return true when this Command no longer needs to run execute()
    protected boolean isFinished() {
        return true;
    }

    // Called once after isFinished returns true
    protected void end() {
    	Robot.driveTrain.set(0);
    }

    // Called when another command which requires one or more of the same
    // subsystems is scheduled to run
    protected void interrupted() {
    }
}