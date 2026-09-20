cmake_minimum_required(VERSION 3.8)
project(ur3_custom_control)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 1. Dependencias ROS 2
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(controller_interface REQUIRED)
find_package(hardware_interface REQUIRED)
find_package(pluginlib REQUIRED)
find_package(realtime_tools REQUIRED)
find_package(eigen3_cmake_module REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(std_msgs REQUIRED)

# 2. CONFIGURACIÓN ONNX RUNTIME (Ruta Local Confirmada)
set(ORT_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/third_party/onnxruntime")
set(ORT_INCLUDE_DIR "${ORT_ROOT}/include")
set(ORT_LIB_DIR "${ORT_ROOT}/lib")

# Buscar la librería exacta que vimos en tu captura (libonnxruntime.so.1.16.3)
# El 'glob' ayuda a encontrarla aunque cambie el nombre exacto de la versión
file(GLOB ORT_LIBS "${ORT_LIB_DIR}/libonnxruntime.so*")

if(NOT ORT_LIBS)
    message(FATAL_ERROR "¡ERROR! No encuentro librerías en ${ORT_LIB_DIR}. Revisa la Fase 1.")
else()
    message(STATUS "Librería ONNX encontrada en: ${ORT_LIBS}")
endif()

# 3. Crear la Librería del Paquete (Incluye AMBOS controladores)
add_library(ur3_custom_control SHARED
  src/ur3_custom_controller.cpp
  src/ur3_neural_controller.cpp
)

# 4. Incluir cabeceras (Headers)
target_include_directories(ur3_custom_control PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  ${Eigen3_INCLUDE_DIRS}
  ${ORT_INCLUDE_DIR}  # Cabeceras de ONNX
)

# 5. Linkear librerías
target_link_libraries(ur3_custom_control
  ${ORT_LIBS}         # Librería de ONNX
)

# 6. Dependencias de Ament
ament_target_dependencies(ur3_custom_control
  rclcpp
  controller_interface
  hardware_interface
  pluginlib
  realtime_tools
  Eigen3
  std_msgs
)

# 7. Exportar Plugin
pluginlib_export_plugin_description_file(controller_interface ur3_custom_control_plugins.xml)

# 8. INSTALACIÓN (Copiar archivos al sistema ROS)
install(TARGETS ur3_custom_control
  EXPORT export_ur3_custom_control
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

install(DIRECTORY include/ DESTINATION include)

# IMPORTANTE: Instalar la librería .so de ONNX para que ROS la encuentre al ejecutar
install(FILES ${ORT_LIBS} DESTINATION lib)

# IMPORTANTE: Instalar la carpeta config (donde está el cerebro .onnx)
#install(DIRECTORY config/ DESTINATION share/${PROJECT_NAME})

# En lugar de instalar la carpeta completa, instalamos los archivos específicos
install(DIRECTORY config/  
  DESTINATION share/${PROJECT_NAME}/config
)

# Instalar el XML de plugins
install(FILES ur3_custom_control_plugins.xml DESTINATION share/${PROJECT_NAME})

ament_package()