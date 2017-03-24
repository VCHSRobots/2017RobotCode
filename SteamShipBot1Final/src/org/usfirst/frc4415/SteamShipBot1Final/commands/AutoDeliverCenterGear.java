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
import java.util.ArrayList;

import edu.wpi.first.wpilibj.Encoder;
import edu.wpi.first.wpilibj.RobotDrive;
import edu.wpi.first.wpilibj.Timer;
import edu.wpi.first.wpilibj.command.Command;

import org.usfirst.frc4415.SteamShipBot1Final.GeneralController;
import org.usfirst.frc4415.SteamShipBot1Final.PIDController;
import org.usfirst.frc4415.SteamShipBot1Final.PIDRobotDriveMove;
import org.usfirst.frc4415.SteamShipBot1Final.Robot;
import org.usfirst.frc4415.SteamShipBot1Final.TimeDelay;

import com.kauailabs.navx.frc.AHRS;

/**
 *
 */
public class AutoDeliverCenterGear extends Command {
	
	RobotDrive robotDrive = Robot.driveTrain.getRobotDrive();
	ArrayList<GeneralController> autoProgram;
	Encoder encoder = Robot.driveTrain.getEncoder();
	int autoStage = 0;
	double inchesToTicks = Robot.tableReader.get("inchestoticks", 9.7073);
	double ticksToInches = 1/inchesToTicks;

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_DECLARATIONS
 
    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_DECLARATIONS

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTOR
    public AutoDeliverCenterGear() {

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTOR
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_SETTING

        // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_SETTING
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=REQUIRES

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=REQUIRES
    	requires(Robot.driveTrain);
    }

    // Called just before this Command runs the first time
    protected void initialize() {
    	autoStage = 0;
    	double pGain = Robot.tableReader.get("pgainmove", .01);
    	double deadband = Robot.tableReader.get("deadbandmove", 0.18);
    	double clipping = Robot.tableReader.get("clippingmove", 0.75);
    	autoProgram = new ArrayList<>();
    	
    	// move towards gear
    	autoProgram.add(new PIDRobotDriveMove(
    			robotDrive, 400, 10, 5000));
    	autoProgram.get(0).setPGain(pGain);
    	autoProgram.get(0).setDeadband(deadband);
    	autoProgram.get(0).setClipping(clipping);
    	
    	// slow move toward gear based on timeout
    	autoProgram.add(new PIDRobotDriveMove(
    			robotDrive, 99999, 0, 1000));
    	autoProgram.get(1).setPGain(pGain);
    	autoProgram.get(1).setDeadband(deadband);
    	autoProgram.get(1).setClipping(Robot.tableReader.get("clippingmoveslow", 0.4));
    	
    	// pause 
    	autoProgram.add(new TimeDelay(500));
    	
    	// back up from gear
    	autoProgram.add(new PIDRobotDriveMove(
    			robotDrive, -100, 10, 5000));
    	autoProgram.get(3).setPGain(pGain);
    	autoProgram.get(3).setDeadband(deadband);
    	autoProgram.get(3).setClipping(clipping);    	
    }

    // Called repeatedly when this Command is scheduled to run
    protected void execute() {
	    if(autoStage < autoProgram.size()){
	    	autoProgram.get(autoStage).run(encoder.get());
	    	if(autoStage==1 && autoProgram.get(autoStage).isDone()){
	    		Robot.gearHandler.gearRelease();
	    	}
	    	System.out.println(autoProgram.get(autoStage));
	    	Robot.logf(autoProgram.get(autoStage).toString());
	    	if(autoProgram.get(autoStage).isDone()){
	    		autoStage++;
	    	}
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
