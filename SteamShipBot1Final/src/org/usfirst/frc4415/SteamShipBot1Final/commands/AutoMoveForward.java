// RobotBuilder Version: 2.0
//
// This file was generated by RobotBuilder. It contains sections of
// code that are automatically generated and assigned by robotbuilder.
// These sections will be updated in the future when you export to
// Java from RobotBuilder. Do not put any code or make any change in
// the blocks indicating autogenerated code or it will be lost on an
// update. Deleting the comments indicating the section will prevent
// it from being updated in the future.


package org.usfirst.frc4415.SteamShipBot1Final.commands;
import edu.wpi.first.wpilibj.Encoder;
import edu.wpi.first.wpilibj.RobotDrive;
import edu.wpi.first.wpilibj.command.Command;

import org.usfirst.frc4415.SteamShipBot1Final.PIDRobotDriveMove;
import org.usfirst.frc4415.SteamShipBot1Final.Robot;

/**
 *
 */
public class AutoMoveForward extends Command {
	
	RobotDrive robotDrive = Robot.driveTrain.getRobotDrive();
	Encoder encoder = Robot.driveTrain.getEncoder();
	PIDRobotDriveMove pidMove = new PIDRobotDriveMove(
			robotDrive, 400, 10, 5000);
    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_DECLARATIONS
 
    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_DECLARATIONS

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTOR
    public AutoMoveForward() {

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTOR
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_SETTING

        // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_SETTING
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=REQUIRES

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=REQUIRES
    	requires(Robot.driveTrain);
    }

    // Called just before this Command runs the first time
    protected void initialize() {
    	Robot.logf("Running \"AutoMoveForward\"");
    	System.out.println("Running AutoMoveForward");
    	pidMove.setPGain(Robot.tableReader.get("pgainmove", 0.01));
    	pidMove.setDeadband(Robot.tableReader.get("deadbandmove", 0.18));
    	pidMove.setClipping(Robot.tableReader.get("clippingmove", 0.5));
    }

    // Called repeatedly when this Command is scheduled to run
    protected void execute() {
    	if(!pidMove.isDone()){
    		pidMove.run(encoder.get());
        	Robot.logf(pidMove.toString());
        	System.out.println(pidMove);
    	}
    }

    // Make this return true when this Command no longer needs to run execute()
    protected boolean isFinished() {
        return false;
    }

    // Called once after isFinished returns true
    protected void end() {
    	Robot.driveTrain.set(0);
    }

    // Called when another command which requires one or more of the same
    // subsystems is scheduled to run
    protected void interrupted() {
    	end();
    }
}
