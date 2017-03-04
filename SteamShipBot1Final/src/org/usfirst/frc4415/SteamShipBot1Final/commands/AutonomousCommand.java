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
import edu.wpi.first.wpilibj.Timer;
import edu.wpi.first.wpilibj.command.Command;
import org.usfirst.frc4415.SteamShipBot1Final.Robot;

/**
 *
 */
public class AutonomousCommand extends Command {

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_DECLARATIONS
 
    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_DECLARATIONS

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTOR
    public AutonomousCommand() {

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTOR
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_SETTING

        // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_SETTING
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=REQUIRES

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=REQUIRES
    }

    // Called just before this Command runs the first time
    protected void initialize() {
    	
    	Robot.gearHandler.autoGearGrab();
    	Timer.delay(.5);
    	Robot.gearHandler.autoHandlerOut();
    	
    	Timer.delay(.5);
    	
    	Robot.driveTrain.autoDriveLeft();
		Timer.delay(1);
		Robot.driveTrain.autoDriveForward();
		
		Timer.delay(1);
		
		Robot.gearHandler.autoGearRelease();
		Timer.delay(.5);
		Robot.gearHandler.autoHandlerIn();
		
		Timer.delay(.5);
		
		Robot.driveTrain.autoDriveBackward();
		
		Timer.delay(.5);
		
		Robot.shooter.autoSet();
		Timer.delay(.5);
		Robot.blender.autoShootBlend();
		
		Timer.delay(8);
		Robot.shooter.autoSetOff();
    	
    	
    	
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
    }

    // Called when another command which requires one or more of the same
    // subsystems is scheduled to run
    protected void interrupted() {
    }
}
