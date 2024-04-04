# Use Ubuntu as base image
FROM ubuntu:latest

# Set environment variable to prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV LAMBDA_FUNCTIONS_DIR /lambda_functions
ENV OUTPUT_DIR /output

# Install required packages
RUN apt-get update && \
    apt-get install -y \
    python3.10 \
    python3.10-distutils \
    python3.10-dev \
    python3.10-venv \
    python3-pip \
    zip \
    nuget

# Alias python3.10 to python3 and pip3.10 to pip3
RUN if [ ! -e /usr/bin/python3 ]; then \
        ln -s /usr/bin/python3.10 /usr/bin/python3; \
    fi && \
    ln -sf /usr/bin/pip3.10 /usr/bin/pip3

# Create the directory structure
RUN mkdir -p $LAMBDA_FUNCTIONS_DIR
RUN mkdir -p $OUTPUT_DIR

COPY export_rds_to_s3 /lambda_functions/export_rds_to_s3
COPY get_secret /lambda_functions/get_secret


# Set the working directory
WORKDIR $LAMBDA_FUNCTIONS_DIR

#Print Current working Directory
RUN pwd

RUN ls -lrt

RUN temp_dir=$(mktemp -d)

# # Install Python dependencies for each Lambda function
# RUN for function_dir in $(find . -maxdepth 1 -mindepth 1 -type d -not -name '.*'); do \
#         (cd $function_dir && \
#         cp * $temp_dir && \
#         pip3 install -r requirements.txt -t $temp_dir && \
#         zip -r "$function_dir.zip" $temp_dir/* && \
#         nuget pack "$function_dir.nuspec"); \
#     done

# RUN for function_dir in $(find . -maxdepth 1 -mindepth 1 -type d -not -name '.*'); do \
#     # Create a unique temporary directory for each function
#     function_temp_dir=$(mktemp -d) && \ 
#     # Copy files to the temporary directory
#     cp -r $function_dir/* $function_temp_dir && \ 
#     # Install Python dependencies for the Lambda function
#     pip3 install -r $function_temp_dir/requirements.txt -t $function_temp_dir && \  
#     # Create a ZIP file for the Lambda function
#     zip -r "$function_dir.zip" $function_temp_dir/* && \
#     # Pack a NuGet package for the Lambda function
#     nuget pack "$function_dir.nuspec" && \
#     # Clean up the temporary directory for the function
#     rm -r $function_temp_dir; \
#     done

RUN for function_dir in $(find . -maxdepth 1 -mindepth 1 -type d -not -name '.*'); do \
        mkdir -p "$function_dir/package" && \
        cp -r "$function_dir"/* "$function_dir/package" && \
        pip3 install -r "$function_dir/package/requirements.txt" -t "$function_dir/package" && \
        zip -r "$function_dir.zip" "$function_dir/package/"* && \
        nuget pack "$function_dir.nuspec"; \
    done


# # Package Lambda functions and put them in NuGet packages
# RUN for function_dir in $(find . -maxdepth 1 -mindepth 1 -type d -not -name '.*'); do \
#         (cd $function_dir && \
#         zip -r "$function_dir.zip" * && \
#         nuget pack "$function_dir.nuspec"); \
#     done

RUN ls -lrt

# Copy NuGet packages to the output directory
RUN cp -r $LAMBDA_FUNCTIONS_DIR/* $OUTPUT_DIR