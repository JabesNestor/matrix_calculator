import flet as ft
import numpy as np


def main(page: ft.Page):
    page.title = "Calculadora de Matrices"
    matrices = []  # Para almacenar las matrices
    page.theme_mode = "dark"    
    # Crear contenedor principal
    main_container = ft.Column(scroll=True)
    
    def create_matrix_inputs(rows, cols):
        matrix_inputs = []
        for i in range(rows):
            row_inputs = []
            for j in range(cols):
                input_field = ft.TextField(
                    width=50,
                    height=50,
                    text_align=ft.TextAlign.CENTER,
                    value="0"
                )
                row_inputs.append(input_field)
            matrix_inputs.append(ft.Row(controls=row_inputs))
        return ft.Column(controls=matrix_inputs)

    def add_matrix(e):
        # Crear controles para dimensiones
        rows_input = ft.TextField(label="Filas", width=100, value="2")
        cols_input = ft.TextField(label="Columnas", width=100, value="2")
        
        def create_matrix_with_dimensions(e):
            try:
                rows = int(rows_input.value)
                cols = int(cols_input.value)
                matrix_container = ft.Container(
                    content=ft.Column([
                        ft.Text(f"Matriz {len(matrices) + 1}"),
                        create_matrix_inputs(rows, cols)
                    ]),
                    
                    padding=10,
                    border=ft.border.all(1)
                )
                matrices.append(matrix_container)
                main_container.controls.append(matrix_container)
                dialog.open = False
                page.update()
            except ValueError:
                print("Por favor ingrese números válidos")
        
        # Diálogo para dimensiones
        dialog = ft.AlertDialog(
            title=ft.Text("Dimensiones de la matriz"),
            content=ft.Column([
                rows_input,
                cols_input,
                ft.ElevatedButton("Crear", on_click=create_matrix_with_dimensions)
            ])
        )
        
        page.dialog = dialog
        dialog.open = True
        page.update()

    def delete_matrix(e):
        if matrices:
            matrix = matrices.pop()
            main_container.controls.remove(matrix)
            page.update()

    def get_matrix_values(matrix_inputs):
        values = []
        for row in matrix_inputs.content.controls[1].controls:
            row_values = []
            for input_field in row.controls:
                try:
                    row_values.append(float(input_field.value))
                except ValueError:
                    return None
            values.append(row_values)
        return np.array(values)

    def calculate(e, operation):
        if len(matrices) < 1:
            return
        
        try:
            if operation in ['inversa', 'det', 'rango', 'traza']:
                matrix = get_matrix_values(matrices[0])
                if matrix is None:
                    return
                
                if operation == 'inversa':
                    result = np.linalg.inv(matrix)
                elif operation == 'det':
                    result = np.linalg.det(matrix)
                elif operation == 'rango':
                    result = np.linalg.matrix_rank(matrix)
                elif operation == 'traza':
                    result = np.trace(matrix)
                
                # Mostrar resultado
                result_text.value = f"Resultado: {result}"
                page.update()
            
            elif len(matrices) >= 2:  # Operaciones con dos matrices
                matrix1 = get_matrix_values(matrices[0])
                matrix2 = get_matrix_values(matrices[1])
                if matrix1 is None or matrix2 is None:
                    return
                
                if operation == 'multiplicacion':
                    result = np.matmul(matrix1, matrix2)
                elif operation == 'suma':
                    result = np.add(matrix1, matrix2)
                elif operation == 'resta':
                    result = np.subtract(matrix1, matrix2)
                
                result_text.value = f"Resultado: {result}"
                page.update()
                
        except Exception as e:
            result_text.value = f"Error: {str(e)}"
            page.update()

    # Crear botones y controles
    add_matrix_btn = ft.ElevatedButton("Agregar Matriz", on_click=add_matrix)
    delete_matrix_btn = ft.ElevatedButton("Eliminar Matriz", on_click=delete_matrix)
    
    # Botones de operaciones
    operations_row = ft.Row([
        ft.ElevatedButton("Inversa", on_click=lambda e: calculate(e, 'inversa')),
        ft.ElevatedButton("Determinante", on_click=lambda e: calculate(e, 'det')),
        ft.ElevatedButton("Rango", on_click=lambda e: calculate(e, 'rango')),
        ft.ElevatedButton("Traza", on_click=lambda e: calculate(e, 'traza')),
        ft.ElevatedButton("Multiplicación", on_click=lambda e: calculate(e, 'multiplicacion')),
        ft.ElevatedButton("Suma", on_click=lambda e: calculate(e, 'suma')),
        ft.ElevatedButton("Resta", on_click=lambda e: calculate(e, 'resta')),
    ])
    
    result_text = ft.Text("Resultado: ")
    
    # Agregar controles a la página
    page.add(
        ft.Row([add_matrix_btn, delete_matrix_btn]),
        operations_row,
        main_container,
        result_text
    )

ft.app(target=main)

