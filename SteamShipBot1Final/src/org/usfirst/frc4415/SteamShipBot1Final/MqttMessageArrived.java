// --------------------------------------------------------------------
// MqttMessageArrived.java -- Interface for MQTT messages
//
// Created 03/20/17 DLB
// -------------------------------------------------------------------

package org.usfirst.frc4415.SteamShipBot1Final;

public interface MqttMessageArrived {
	void OnNewMessage(MqttMsg m);
}
