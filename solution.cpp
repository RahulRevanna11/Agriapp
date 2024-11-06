#include <iostream>
using namespace std;

int computeSizeOnDisk(int cluster_size, int file_size) {
    // If file is empty, no clusters needed
    if (file_size == 0) {
        return 0;
    }
    
    // Calculate number of clusters needed (using ceiling division)
    // The formula (a + b - 1) / b gives us ceiling division for positive numbers
    int num_clusters = (file_size + cluster_size - 1) / cluster_size;
    
    // Calculate total size on disk
    int size_on_disk = num_clusters * cluster_size;
    
    return size_on_disk;
}

int main() {
    int cluster_size = 512; // Size of each cluster in bytes
    int file_size = 1500;   // Size of the file in bytes

    int result = computeSizeOnDisk(cluster_size, file_size);
    cout << "Size on disk: " << result << " bytes" << endl; // Print the result
    return 0;
}
