import tinyWinToast.tinyWinToast

if __name__ == "__main__":
	toast = tinyWinToast.tinyWinToast.Toast()
	toast.setTitle("TEST TITLE", maxLines=1)
	toast.setMessage("TEST MESSAGE", maxLines=1)
	toast.addText("TEST OTHER TEXT", maxLines=1)
	toast.show()