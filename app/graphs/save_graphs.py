from pathlib import Path

# ------------------------
# Save Workflow Visualization
# ------------------------
def save_workflow_graph(workflow, filename="workflow.png", outdir="../graphs"):
    """
    Save workflow graph as PNG, SVG, or JPG outside current directory.
    :param workflow: Compiled LangGraph workflow
    :param filename: Name of file (e.g., 'workflow.png', 'workflow.svg', 'workflow.jpg')
    :param outdir: Directory path relative or absolute
    """
    out_path = Path(outdir).resolve()
    out_path.mkdir(parents=True, exist_ok=True)

    ext = Path(filename).suffix.lower()

    if ext == ".png":
        data = workflow.get_graph().draw_mermaid_png()
    # elif ext == ".svg":
    #     data = workflow.get_graph().draw_mermaid_svg()
    elif ext in [".jpg", ".jpeg"]:
        # Convert PNG bytes -> JPG
        from PIL import Image
        import io
        png_bytes = workflow.get_graph().draw_mermaid_png()
        img = Image.open(io.BytesIO(png_bytes))
        rgb_img = img.convert("RGB")
        jpg_file = out_path / filename
        rgb_img.save(jpg_file, format="JPEG")
        print(f"✅ Workflow saved at: {jpg_file}")
        return
    else:
        raise ValueError("Unsupported file format. Use .png, .svg, or .jpg")

    # Save raw bytes
    file_path = out_path / filename
    with open(file_path, "wb") as f:
        f.write(data)
    print(f"✅ Workflow saved at: {file_path}")


