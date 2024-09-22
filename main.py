import pyproj
import shutil
import os
import sys

def lat_lon_to_utm(lat, lon):
    # Create a UTM projection based on the longitude
    utm_proj = pyproj.Proj(proj='utm', zone=int((lon + 180) / 6) + 1, ellps='WGS84')
    
    # Ensure proper precision by using float
    easting, northing = utm_proj(lon, lat)
    
    return float(easting), float(northing)

def main():

    field_path = "/home/davidwedel/Documents/QtAgOpenGPS/Fields"

    field_name = "Hills South"

    source_field = os.path.join(field_path, field_name)

    destination_path = "/home/davidwedel/Documents/FieldOriginHash"

    destination_dir = os.path.join(destination_path, field_name)

    if os.path.exists(destination_dir):
        print(f"Field {field_name} already exists. Deleting.")
        shutil.rmtree(destination_dir)

    shutil.copytree(source_field, destination_dir) #create a copy of the original field
    
    with open(os.path.join(destination_path, field_name, "Field.txt"), "r") as field:
        #read all lines from the file
        lines = field.readlines()


        # Access the 6th line (index 5 since Python uses 0-based indexing)
        if len(lines) >= 9:
            start_fix = lines[8]
            print("Original StartFix:", start_fix.strip())
        else:
            print("The file has fewer than 6 lines.")
            sys.exit(1)
 

    start_fix = start_fix.strip().split(",")

    lat_old, lon_old = float(start_fix[0]), float(start_fix[1])
    lat_new, lon_new = float(38.44538), float(-97.49394) # 38.44538, -97.49394 # new field origin

    print(f"Old StartFix: {lat_old}, {lon_old}")
    print(f"New StartFix: {lat_new}, {lon_new}")

    # Convert to UTM
    easting_old, northing_old = lat_lon_to_utm(lat_old, lon_old)
    easting_new, northing_new = lat_lon_to_utm(lat_new, lon_new)

    # Calculate differences
    easting_diff = float(easting_old - easting_new)
    northing_diff = float(northing_old - northing_new)

    print(f"Difference in Easting : {easting_diff} meters")
    print(f"Difference in Northing : {northing_diff} meters")


    #set the StartFix in the Field.txt to the new StartFix

    lines[8] = f"{lat_new},{lon_new}\n"
    
    print(f"Changed StartFix to: {lines[8]}")

    with open(os.path.join(destination_path, field_name, "Field.txt"), "w") as field:
        field.writelines(lines)

    print("Done with Field.txt")
    
    #starting with Boundary.txt

    #$Boundary
    #False
    #824                        number of points
    #-631.348,118.125,3.14613   easting, northing, heading

    with open(os.path.join(destination_path, field_name, "Boundary.txt"), "r") as boundary:
        #read all lines from the file
        lines = boundary.readlines()

        updated_lines = []
        i = 0

        while i < len(lines[i]):
            
            #copy the current line
            updated_lines.append(lines[i])
            print(lines[i])

             # Check if the line is a count line (it should be an integer)
            try:
                count = int(lines[i + 1].strip())
                print("countline:", count)
            except ValueError:
                print("Not a count line. Skipping.")
                count = 0 

            for j in range(count):
                if i + 1 + j < len(lines):  # Ensure we don't go out of bounds
                    values = lines[i + 2 + j].strip().split(',')
                    # Convert the first two values to float and add the offsets
                    northing = float(values[0]) + northing_diff
                    easting = float(values[1]) + easting_diff
                    third_value = values[2]
                    # Create the updated line
                    updated_line = f"{northing:.3f},{easting:.3f},{third_value}\n"
                    updated_lines.append(updated_line)                

            #move to the next section
            i += count + 2
        
    # Write the updated lines back to the file
    with open(os.path.join(destination_path, field_name, "Boundary.txt"), 'w') as file:
        file.writelines(updated_lines)

    print("Done with Boundary.txt")        


if __name__ == "__main__":
    main()


