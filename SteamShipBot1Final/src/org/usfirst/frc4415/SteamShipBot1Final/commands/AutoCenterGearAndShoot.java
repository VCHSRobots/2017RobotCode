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
import org.usfirst.frc4415.SteamShipBot1Final.PIDRobotDriveRotate;
import org.usfirst.frc4415.SteamShipBot1Final.PIDTurret;
import org.usfirst.frc4415.SteamShipBot1Final.Robot;
import org.usfirst.frc4415.SteamShipBot1Final.TimeDelay;
import org.usfirst.frc4415.SteamShipBot1Final.subsystems.Turret;

import com.kauailabs.navx.frc.AHRS;

/**
 *
 */
public class AutoCenterGearAndShoot extends Command {
	
	ArrayList<GeneralController> autoProgram;
	RobotDrive robotDrive = Robot.driveTrain.getRobotDrive();
	Turret turret = Robot.turret;
	Encoder encoder = Robot.driveTrain.getEncoder();
	AHRS navX = Robot.navX;
	int autoStage = 0;
	final int BOILER = 1;
	final int PEG =2;
	double inchesToTicks = Robot.tableReader.get("inchestoticks", 9.7073);
	double ticksToInches = 1/inchesToTicks;

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_DECLARATIONS
 
    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_DECLARATIONS

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTOR
    public AutoCenterGearAndShoot() {

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTOR
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_SETTING

        // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_SETTING
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=REQUIRES

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=REQUIRES
    	requires(Robot.driveTrain);
    	requires(Robot.turret);
    }

    // Called just before this Command runs the first time
    protected void initialize() {
    	
    	System.out.println("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nRUNNING CENTER GEAR AND SHOOT!!! \n\n\n\n\n");
    	
    	autoStage = 0;
    	double pGain = Robot.tableReader.get("pgainmove", .01);
    	double deadband = Robot.tableReader.get("deadbandmove", 0.18);
    	double clipping = Robot.tableReader.get("clippingmove", 0.75);
    	double pGainRotate = Robot.tableReader.get("pgainrotate",  0.3);
    	double deadbandRotate = Robot.tableReader.get("deadbandrotate", 0.3);
    	double clippingRotate = Robot.tableReader.get("clippingrotate", 1);
    	Robot.targetReportMonitor.selectTarget(BOILER);
    	autoProgram = new ArrayList<>();
    	
    	// quick move toward gear
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
    	autoProgram.get(1).setClipping(clipping);
    	
    	// release gear
    	// center turret
    	// pause
    	autoProgram.add(new TimeDelay(250));
    	
    	// move away from gear
    	autoProgram.add(new PIDRobotDriveMove(
    			robotDrive, -100, 10, 5000));
    	autoProgram.get(3).setPGain(pGain);
    	autoProgram.get(3).setDeadband(deadband);
    	autoProgram.get(3).setClipping(clipping);  
    	
    	// rotate towards boiler
    	if(Robot.autoParams.getSide().equals("blue")){
    	autoProgram.add(new PIDRobotDriveRotate(
    			robotDrive, 27, true, 10, 5000));
    	} else {
    		autoProgram.add(new PIDRobotDriveRotate(
        			robotDrive, -27, true, 10, 5000));
    	}
    	autoProgram.get(4).setPGain(pGainRotate);
    	autoProgram.get(4).setDeadband(deadbandRotate);
    	autoProgram.get(4).setClipping(clippingRotate); 
    	
    	// move towards boiler
    	autoProgram.add(new PIDRobotDriveMove(
    			robotDrive, -200, 10, 5000));
    	autoProgram.get(5).setPGain(pGain);
    	autoProgram.get(5).setDeadband(deadband);
    	autoProgram.get(5).setClipping(clipping);
    	
    	// switch to mecanum, aim drivetrain at boiler
    	autoProgram.add(new PIDRobotDriveRotate(
    			robotDrive, 0, false, 200, 3000));
    	autoProgram.get(6).setPGain(Robot.tableReader.get("pgainrotatetarget",  0.0015));
    	autoProgram.get(6).setDeadband(Robot.tableReader.get("deadbandrotatetarget",  0.1));
    	autoProgram.get(6).setClipping(1);
    	
    	// aim turret at boiler
    	autoProgram.add(new PIDTurret(
    			turret, 0, 4, 3000));
    	autoProgram.get(7).setPGain(Robot.tableReader.get("pgainturret", 0.01));
    	autoProgram.get(7).setDeadband(Robot.tableReader.get("deadbandturret", 0.05));
    	autoProgram.get(7).setClipping(1);
    }

    // Called repeatedly when this Command is scheduled to run
    protected void execute() {
	    if(autoStage < autoProgram.size()){
	    	double feedback = 0;
	    	if(autoStage==0 || autoStage==1 ||autoStage==3 ||autoStage==5) feedback = encoder.get();
	    	else if (autoStage==4) feedback = Robot.gyroAngle;
	    	else if (autoStage==6 || autoStage==7) feedback = Robot.targetReportMonitor.report().x1000() * -1.0;
	    	else feedback = 0;
	    	autoProgram.get(autoStage).run(feedback);
	    	if(autoStage==1 && autoProgram.get(autoStage).isDone()){
	    		Robot.gearHandler.gearRelease();
	    		//Robot.turret.reset();
	    	}
	    	if(autoStage==3 && autoProgram.get(autoStage).isDone()){
	    		Robot.gearHandler.handlerIn();
	    		Robot.shooter.toggleShooter();
	    	}
	    	if(autoStage==5 && autoProgram.get(autoStage).isDone()){
	    		Robot.driveTrain.setMecanum();
	    		Robot.driveTrain.invertMotorsArcade();
	    		Robot.target.on();
	    	}
	    	if(autoStage==7 && autoProgram.get(autoStage).isDone()){
	    		Robot.turret.turn(0);
	    		Robot.target.off();
	    	}
	    	System.out.println(autoProgram.get(autoStage));
	    	Robot.logf(autoProgram.get(autoStage).toString());
	    	if(autoProgram.get(autoStage).isDone()){
	    		autoStage++;
	    	}
	    } else {
	    	Robot.blender.set(Robot.tableReader.get("blender", -1));
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
