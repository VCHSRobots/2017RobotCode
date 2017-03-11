package org.usfirst.frc4415.SteamShipBot1Final.commands;

import org.usfirst.frc4415.SteamShipBot1Final.*;

import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;

public class ShooterThread extends Thread {
	// positve set value the shooter correctly and causes encoder value to decrease
	public void run(){
		while(true){
			double defaultRPM = 1000;
			double setpoint = Robot.shooter.getSetpoint();
			//double setpoint = Robot.tableReader.get("shooter", defaultRPM);
			double minThreshold = 0.95*setpoint;
			double maxThreshold = 0.98*setpoint;
			boolean isArmed = Robot.shooter.getIsArmed();
			
			int sleepLength = 5; // in milliseconds
			
			if(Robot.shooter.getShooterToggle()){
				Robot.shooter.setSpeedMode();
				double currentSpeed = Robot.shooter.getEncoderSpeed();
				if(!isArmed){
					Robot.shooter.set(setpoint);
					if(Math.abs(currentSpeed) > Math.abs(minThreshold)){
						Robot.shooter.arm();
						System.out.println("Shooter Armed!");
					}
				}
				if(isArmed){
					if(Math.abs(currentSpeed) > Math.abs(minThreshold)){
						Robot.shooter.set(setpoint);
					} else {
						Robot.shooter.setThrottleMode();
						Robot.shooter.set(1);
						while(Math.abs(Robot.shooter.getEncoderSpeed())<Math.abs(maxThreshold)){
							try {
								System.out.println("BOOOOSTERS ON!!!!!");
								SmartDashboard.putNumber("Output Voltage", Robot.shooter.getOutputVoltage());
								SmartDashboard.putNumber("RPM", Robot.shooter.getEncoderSpeed());
								Thread.sleep(sleepLength);
							} catch (InterruptedException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
							}
						}
						Robot.shooter.setSpeedMode();
						Robot.shooter.set(setpoint);
					}
				}
			
			
			} else {
				Robot.shooter.setThrottleMode();
				Robot.shooter.set(0);
			}
			SmartDashboard.putNumber("Output Voltage", Robot.shooter.getOutputVoltage());
			SmartDashboard.putNumber("RPM", Robot.shooter.getEncoderSpeed());
			try {
				Thread.sleep(sleepLength);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

		}
	}
		
}