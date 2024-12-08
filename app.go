package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"os/exec"

	"github.com/gin-gonic/gin"
)

type Config struct {
	ServerURL string `json:"server_url"`
	APIKey    string `json:"api_key"`
}

type ScanData struct {
	OSName         string `json:"os_name"`
	OSVersion      string `json:"os_version"`
	LastUpdated    string `json:"last_updated"`
	AvailableDisk  string `json:"available_disks"`
	FreeDiskSpace  string `json:"free_disk_space"`
	TotalDiskSpace string `json:"total_disk_space"`
}

type Device struct {
	Hostname   string `json:"hostname"`
	MacAddress string `json:"mac_address"`
}

var configFilePath = "config.json"

func main() {
	r := gin.Default()

	// Initialize app with a welcome screen
	r.GET("/", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "Welcome to the Desktop App!",
		})
	})

	// Load the previous configuration
	var config Config
	if err := loadConfig(&config); err != nil {
		fmt.Println("Error loading config:", err)
	}

	// Route to register device
	r.POST("/register_device", func(c *gin.Context) {
		hostname, _ := os.Hostname()
		macAddress := "XX:XX:XX:XX:XX:XX" // This should be fetched dynamically
		device := Device{Hostname: hostname, MacAddress: macAddress}

		// Call register device API
		if err := registerDevice(device); err != nil {
			c.JSON(500, gin.H{"error": err.Error()})
			return
		}

		// Save configuration (Server URL, API Key)
		err := saveConfig(config)
		if err != nil {
			c.JSON(500, gin.H{"error": "Unable to save config"})
			return
		}

		c.JSON(200, gin.H{"message": "Device registered successfully!"})
	})

	// Route to perform scan
	r.POST("/scan", func(c *gin.Context) {
		// Check if device is registered
		if !isDeviceRegistered() {
			c.JSON(400, gin.H{"error": "Device not registered"})
			return
		}

		// Fetch OS Information
		scanData, err := getOSInfo()
		if err != nil {
			c.JSON(500, gin.H{"error": "Unable to fetch OS info"})
			return
		}

		// Save scan results
		err = saveScanResults(scanData)
		if err != nil {
			c.JSON(500, gin.H{"error": "Unable to save scan results"})
			return
		}

		c.JSON(200, gin.H{"message": "Scan results saved successfully!"})
	})

	// Start the web server
	r.Run(":8080")
}

func loadConfig(config *Config) error {
	if _, err := os.Stat(configFilePath); os.IsNotExist(err) {
		return err
	}

	file, err := os.Open(configFilePath)
	if err != nil {
		return err
	}
	defer file.Close()

	decoder := json.NewDecoder(file)
	return decoder.Decode(config)
}

func saveConfig(config Config) error {
	file, err := os.Create(configFilePath)
	if err != nil {
		return err
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	return encoder.Encode(config)
}

func registerDevice(device Device) error {
	url := fmt.Sprintf("%s/register_device", "http://localhost:8000")
	deviceData, err := json.Marshal(device)
	if err != nil {
		return err
	}

	resp, err := http.Post(url, "application/json", bytes.NewBuffer(deviceData))
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return fmt.Errorf("Failed to register device")
	}

	return nil
}

func getOSInfo() (ScanData, error) {
	var scanData ScanData

	// Fetch OS name and version
	cmd := exec.Command("uname", "-s")
	output, err := cmd.Output()
	if err != nil {
		return scanData, err
	}
	scanData.OSName = string(output)

	cmd = exec.Command("uname", "-r")
	output, err = cmd.Output()
	if err != nil {
		return scanData, err
	}
	scanData.OSVersion = string(output)

	// Fetch Disk Info
	cmd = exec.Command("df", "-h")
	output, err = cmd.Output()
	if err != nil {
		return scanData, err
	}
	scanData.AvailableDisk = string(output)

	// Other info like Free/Total Disk Space
	// Parsing df -h output or using any library to get disk stats

	return scanData, nil
}

func saveScanResults(scanData ScanData) error {
	url := fmt.Sprintf("%s/save_scan_results", "http://localhost:8000")
	data, err := json.Marshal(scanData)
	if err != nil {
		return err
	}

	resp, err := http.Post(url, "application/json", bytes.NewBuffer(data))
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return fmt.Errorf("Failed to save scan results")
	}

	return nil
}

func isDeviceRegistered() bool {
	// Check if the device is registered, possibly by verifying the existence of config file
	return true
}
