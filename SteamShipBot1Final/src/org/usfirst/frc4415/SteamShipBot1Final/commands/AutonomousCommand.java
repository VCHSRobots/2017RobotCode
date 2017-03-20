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

import org.usfirst.frc4415.SteamShipBot1Final.PIDController;
import org.usfirst.frc4415.SteamShipBot1Final.PIDRobotDriveMove;
import org.usfirst.frc4415.SteamShipBot1Final.PIDRobotDriveRotate;
import org.usfirst.frc4415.SteamShipBot1Final.Robot;

import com.kauailabs.navx.frc.AHRS;

/**
 *
 */
public class AutonomousCommand extends Command {
	
	ArrayList<PIDController> autoProgram;
	Encoder encoder = Robot.driveTrain.getEncoder();
	AHRS navX = Robot.navX;
	int autoStage = 0;

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_DECLARATIONS
 
    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_DECLARATIONS

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTOR
    public AutonomousCommand() {

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTOR
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_SETTING

        // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_SETTING
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=REQUIRES

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=REQUIRES
    	requires(Robot.driveTrain);
    }

    protected void initialize() {
    	autoStage = 0;
    	RobotDrive robotDrive = Robot.driveTrain.getRobotDrive();
    	navX.reset();
    	double pGain = Robot.tableReader.get("pgain", .01);
    	double deadband = Robot.tableReader.get("deadband", 0.18);
    	double clipping = Robot.tableReader.get("clipping", 0.75);
    	Robot.driveTrain.setArcade();
    	Robot.gearHandler.gearGrab();
    	Robot.gearHandler.handlerOut();
    	
 		autoProgram = new ArrayList<>();
    	autoProgram.add(new PIDRobotDriveMove(
    			robotDrive, 1000, 10, 5000));
    	autoProgram.get(0).setPGain(pGain);
    	autoProgram.get(0).setDeadband(deadband);
    	autoProgram.get(0).setClipping(clipping);
    	
    	autoProgram.add(new PIDRobotDriveRotate(
    			robotDrive, 90, true, 2, 20000));
    	autoProgram.get(1).setPGain(.1);
    	autoProgram.get(1).setDeadband(deadband);
    	autoProgram.get(1).setClipping(clipping);
    	
    	autoProgram.add(new PIDRobotDriveMove(
    			robotDrive, -1000, 10, 5000));
    	autoProgram.get(2).setPGain(pGain);
    	autoProgram.get(2).setDeadband(deadband);
    	autoProgram.get(2).setClipping(clipping);
    	
    	autoProgram.add(new PIDRobotDriveRotate(
    			robotDrive, -90, true, 2, 20000));
    	autoProgram.get(3).setPGain(.1);
    	autoProgram.get(3).setDeadband(deadband);
    	autoProgram.get(3).setClipping(clipping);
    }
    
    protected void execute() {
    	double feedback;
    	if(autoStage == 0 || autoStage == 2) feedback = encoder.get();
    	else feedback = navX.getAngle();
    	autoProgram.get(autoStage).run(feedback);
    	System.out.println(autoProgram.get(autoStage));
    	if(autoProgram.get(autoStage).isDone()){
    		autoStage++;
    	}
    }

    protected boolean isFinished() {
    	if(autoStage == autoProgram.size()){
    		return true;
    	} else return false;
    }

    protected void end() {
    	Robot.driveTrain.set(0);
    }

    protected void interrupted() {
    	end();
    }
}
