import numpy as np

NX = 177
NY = 168
NH = 24
RECL = 4 * NX * NY

def read_landuse_file(file_path):
    with open(file_path, "rb") as f:
        # Read record 1: alon
        f.seek(0)  # First record starts at position 0
        alon_bytes = f.read(RECL)
        alon = np.frombuffer(alon_bytes, dtype=np.float32).reshape(NY, NX)
        
        # Read record 2: alat
        f.seek(RECL)  # Second record starts after first record
        alat_bytes = f.read(RECL)
        alat = np.frombuffer(alat_bytes, dtype=np.float32).reshape(NY, NX)
        
        # Read record 3: rlui
        f.seek(2 * RECL)  # Third record
        rlui_bytes = f.read(RECL)
        rlui = np.frombuffer(rlui_bytes, dtype=np.float32).reshape(NY, NX)
        
        # Read record 4: hgt
        f.seek(3 * RECL)  # Fourth record
        hgt_bytes = f.read(RECL)
        hgt = np.frombuffer(hgt_bytes, dtype=np.float32).reshape(NY, NX)

    return alon, alat, rlui, hgt

def write_landuse_file(file_path, alon, alat, rlui, hgt):
    with open(file_path, "wb") as f:
        # Write record 1: alon
        f.seek(0)
        f.write(alon.astype(np.float32).tobytes())
        # Write record 2: alat
        f.seek(RECL)
        f.write(alat.astype(np.float32).tobytes())
        # Write record 3: rlui
        f.seek(2 * RECL)
        f.write(rlui.astype(np.float32).tobytes())
        # Write record 4: hgt
        f.seek(3 * RECL)
        f.write(hgt.astype(np.float32).tobytes())

def read_landuseF_file(file_path):
    with open(file_path, "rb") as f:
        # Read record 1: frac_r
        f.seek(0)  # First record starts at position 0
        frac_r_bytes = f.read(RECL)
        frac_r = np.frombuffer(frac_r_bytes, dtype=np.float32).reshape(NY, NX)
        
        # Read record 2: frac_u
        f.seek(RECL)  # Second record starts after first record
        frac_u_bytes = f.read(RECL)
        frac_u = np.frombuffer(frac_u_bytes, dtype=np.float32).reshape(NY, NX)

    return frac_r, frac_u

def write_landuseF_file(file_path, frac_r, frac_u):
    with open(file_path, "wb") as f:
        # Write record 1: frac_r
        f.seek(0)
        f.write(frac_r.astype(np.float32).tobytes())
        # Write record 2: frac_u
        f.seek(RECL)
        f.write(frac_u.astype(np.float32).tobytes())

def read_temp_file(file_path):
    temp_data = np.zeros((NH, NY, NX), dtype=np.float32)
    
    with open(file_path, "rb") as f:
        for ih in range(NH):
            # Read record ih+1
            f.seek(ih * RECL)  # Position to the correct record
            temp_bytes = f.read(RECL)
            temp = np.frombuffer(temp_bytes, dtype=np.float32).reshape(NY, NX)
            temp_data[ih, :, :] = temp

    # temp_data[0] is hour 1 (12:00AM MST)
    # temp_data[23] is hour 24 (11:00PM MST)
    temp_data = np.roll(temp_data, shift=-7, axis=0)

    return temp_data