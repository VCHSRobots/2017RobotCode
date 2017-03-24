// --------------------------------------------------------------------
// ShooterRpm.java -- class to calculated shooter rpm based on camera reading.
//
// Created 03/24/17 DLB
// --------------------------------------------------------------------

package org.usfirst.frc4415.SteamShipBot1Final;

public class ShooterRpm {
	// The following is data taken the night before the 2017 Long Beach Competition with the practice robot.
	// If you need different tables, please comment this for documentation.
	private static double[] m_range  = new double[] {    4.0,    5.0,    6.0,    7.0,    8.0,    9.0,   13.5 };
	private static double[] m_angles = new double[] { -300.0, -281.0, -200.0, -133.0,  -72.0,  -30.0,  121.0 };
	private static double[] m_rpms   = new double[] { 1000.0, 1010.0, 1050.0, 1070.0, 1125.0, 1200.0, 1200.0 };
	
	// Given the reported Y value from the camera, returns a RPM to use.
	public static double rpm(double cameraAngle) {
		if (cameraAngle < m_angles[0]) return m_rpms[0];
		int n = m_angles.length;
		if (cameraAngle >= m_angles[n - 1] ) return m_rpms[n - 1];
		for (int i = 0; i < n - 1; i++) {
			if(cameraAngle >= m_angles[i] && cameraAngle <= m_angles[i + 1]) {
				try {
					double da = m_angles[i + 1] - m_angles[i];
					double dr = m_rpms[i + 1] - m_rpms[i];
					double x = (cameraAngle - m_angles[i]) / da;
					double r = m_rpms[i] + x * dr;
					return r;
				}
				catch (ArithmeticException ee) {
					return 1050.0;
				}
			}
		}
		return m_rpms[n - 1];
	}

}
