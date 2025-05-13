from src.core.PipelineComponent import PipelineComponent
import subprocess
class HDFSUploader(PipelineComponent):
        def __init__(self, container_name = 'spark-sql-and-pyspark-using-python3-itvdelab-1' , hdfs_base_path = '/'):
                self.container_name = container_name
                self.hdfs_base_path = hdfs_base_path
                # the parque path should be mounted inside the container
        def process(self, context):
                output_file = context.metadata.get("output_file")
        
                if not output_file:
                        context.add_error("No output file to upload to HDFS")
                        return context
        
                # Construct the command to run inside the container
                command = f"docker exec {self.container_name} hdfs dfs -put {output_file} {self.hdfs_base_path}"
                try:
                        # Run the command using subprocess
                        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

                        # If the command is successful
                        context.add_metadata("hdfs_path", self.hdfs_base_path)
                        context.add_metadata("upload_result", result.stdout)
                        
                except subprocess.CalledProcessError as e:
                        error_message = f"HDFS upload failed: {e.stderr}"
                        context.add_error(error_message)
                        
                return context

        

    